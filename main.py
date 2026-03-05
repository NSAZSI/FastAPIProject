import uvicorn
from contextlib import asynccontextmanager  # 1. 引入上下文管理器
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from app.api.v1.api import api_router
from app.db.base import Base
from app.db.session import engine
from typing import Callable
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from alembic.config import Config
from alembic import command
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
# 2. 定义寿命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 【启动时执行】: 自动创建数据库表
    #async with engine.begin() as conn:
    #   await conn.run_sync(Base.metadata.create_all)
    def run_upgrade():
    # 【自动化升级核心代码】
    # 告诉 Alembic 配置文件在哪里
        alembic_cfg = Config("alembic.ini")
    # 相当于在终端运行了 alembic upgrade head
        command.upgrade(alembic_cfg, "head")

    # 2. 使用 run_in_threadpool 来运行同步的 Alembic 命令
    # 这样它内部触发的协程就能在它自己的环境里正确处理，不会报“未被等待”的错
    await run_in_threadpool(run_upgrade)

    yield  # 这里是分割线，上面是启动逻辑，下面是关闭逻辑

    # 【关闭时执行】: 如果有需要清理的资源（如连接池），写在这里
    pass


# 3. 在初始化 FastAPI 时挂载 lifespan
app = FastAPI(title="Todo Project", lifespan=lifespan)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    # 使用你改好的 9000 端口
    uvicorn.run("main:app", host="127.0.0.1", port=8888, reload=True)

# 2026-03-05: 第一次实弹测试 Webhook 自动触发流水线。