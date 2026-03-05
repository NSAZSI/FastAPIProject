from fastapi import APIRouter
from app.api.v1.endpoints import users, todos # 导入你写的模块

api_router = APIRouter()

# 挂载用户模块
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
# 挂载待办事项模块
api_router.include_router(todos.router, prefix="/todos", tags=["待办事项"])