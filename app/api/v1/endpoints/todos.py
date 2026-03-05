from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.schemas.todo import TodoUpdate  # 别忘了导入新模型
from app.db.session import get_db
from app.models.todo import TodoDB
from app.schemas.todo import TodoCreate, TodoOut
from app.api.v1.endpoints.users import get_current_user  # 引入刚才写好的安保工具
from app.models.user import UserDB

router = APIRouter()


# 1. 创建任务：自动绑定当前登录用户
@router.post("/", response_model=TodoOut)
async def create_todo(
        todo_in: TodoCreate,
        db: AsyncSession = Depends(get_db),
        current_user: UserDB = Depends(get_current_user)  # 关键：只有登录了才能创建
):
    # 将前端数据转为字典，并手动加入当前用户的 ID
    todo_data = todo_in.model_dump()
    todo_data["owner_id"] = current_user.id

    db_todo = TodoDB(**todo_data)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


# 2. 获取任务：只能看到属于“我”的任务
@router.get("/", response_model=List[TodoOut])
async def read_todos(
        db: AsyncSession = Depends(get_db),
        current_user: UserDB = Depends(get_current_user),
        skip: int = 0,  # 新增：跳过多少条记录
        limit: int = 10  # 新增：本次查询多少条记录
):
    # 构造查询语句，加入分页逻辑
    result = await db.execute(
        select(TodoDB)
        .where(
            TodoDB.owner_id == current_user.id,  # 权限隔离：只看自己的
            TodoDB.is_deleted == False  # 逻辑删除过滤：只看没删的
        )
        .offset(skip)  # 跳过前面的记录
        .limit(limit)  # 限制返回的数量
    )

    # 获取查询结果并返回
    return result.scalars().all()





@router.patch("/{todo_id}", response_model=TodoOut)
async def update_todo(
        todo_id: int,
        todo_in: TodoUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: UserDB = Depends(get_current_user)
):
    # 1. 权限校验：查询【属于当前用户】的【特定ID】任务
    result = await db.execute(
        select(TodoDB).where(TodoDB.id == todo_id, TodoDB.owner_id == current_user.id)
    )
    db_todo = result.scalars().first()

    # 2. 越权防护：如果查不到，说明要么任务不存在，要么你试图修改别人的任务
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务未找到或您无权操作此任务"
        )

    # 3. 动态更新：只更新前端传了的字段
    # exclude_unset=True 保证了：如果前端只传了 {"completed": true}，我们就只改这一项
    update_data = todo_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    await db.commit()
    await db.refresh(db_todo)  # 刷新数据，确保返回的是数据库最新的状态
    return db_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        todo_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: UserDB = Depends(get_current_user)
):
    # 1. 查询该用户名下的这个任务
    result = await db.execute(
        select(TodoDB).where(TodoDB.id == todo_id, TodoDB.owner_id == current_user.id)
    )
    db_todo = result.scalars().first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="任务未找到或权限不足")

    # 2. 执行【逻辑删除】：不再调用 db.delete(db_todo)
    db_todo.is_deleted = True

    await db.commit()  # 仅仅是改了个字段值，然后提交
    return None