import os
from dotenv import load_dotenv
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
load_dotenv() # 加载 .env 文件

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession  # 显式指定异步会话类
)

# 依赖注入函数：每次请求时创建一个会话，结束后自动关闭
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session