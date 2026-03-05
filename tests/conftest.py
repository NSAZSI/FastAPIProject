import os

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool  # <--- 魔法子弹！专门对付跨循环报错
from main import app
from app.db.session import get_db
from app.db.base_class import Base

# 1. 初始化引擎时，强制使用 NullPool（禁用连接池）
# 这样每次请求都会新建真实的连接，彻底切断上一个 Loop 的历史包袱
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "mysql+asyncmy://root:123456@localhost:3306/todo_test"
)
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


# 2. 自动建表/删表 (使用全局作用域，仅执行一次)
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()  # 测试结束，销毁引擎


# 3. 覆盖依赖：每个测试用例都会触发这里，生成绝对干净的 Session
@pytest_asyncio.fixture(autouse=True)
async def override_get_db():
    async def _override():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


# 4. 异步测试客户端：每个测试用例分配一个独立的客户端
@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac