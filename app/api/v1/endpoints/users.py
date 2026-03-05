from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token
from app.db.session import get_db  # 获取数据库会话的依赖
from app.models.user import UserDB  # 数据库模型
from app.schemas.user import UserCreate, UserOut  # Pydantic模型

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. 检查用户名是否已存在（面试必写，体现严谨性）
    result = await db.execute(select(UserDB).where(UserDB.username == user_in.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被注册"
        )

    # 2. 加工数据
    user_data = user_in.model_dump()
    plain_password = user_data.pop("password")
    user_data["hashed_password"] = hash_password(plain_password)

    # 3. 保存
    db_user = UserDB(**user_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user




@router.post("/login")
async def login(
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()  # 自动解析用户名和密码
):
    # 1. 在数据库中查找用户
    result = await db.execute(select(UserDB).where(UserDB.username == form_data.username))
    user = result.scalars().first()

    # 2. 验证用户是否存在，以及密码是否正确
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 验证成功，发放 Token
    access_token = create_access_token(data={"sub": user.username})

    # 4. 返回符合 OAuth2 标准的 JSON
    return {"access_token": access_token, "token_type": "bearer"}


# 定义 Token 的来源：告诉 FastAPI 去 /login 接口拿令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


# --- 核心依赖项：获取当前登录用户 ---
async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,  # 使用配置对象的密钥
            algorithms=[settings.ALGORITHM]  # 使用配置对象的算法
        )
        username: str = payload.get("sub")

        if username is None:
            print("❌ Token 中没有找到 username (sub)")
            raise credentials_exception

    except JWTError as e:
        print(f"❌ JWT 解密失败: {str(e)}")
        raise credentials_exception

    # 3. 到数据库核实用户
    result = await db.execute(select(UserDB).where(UserDB.username == username))
    user = result.scalars().first()

    if user is None:
        print(f"❌ 数据库中找不到用户: {username}")
        raise credentials_exception

    return user


# --- 受保护的接口：查看我的个人资料 ---
@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    # 直接返回 current_user，FastAPI 会根据 response_model=UserOut 自动过滤数据
    return current_user