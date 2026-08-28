import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.dependencies import get_db
from app.db.database import Base
from app.main import app

os.environ["DB_URL"] = "sqlite+aiosqlite:///./test2.db"

os.environ["SECRET_KEY"] = "testpassword123adummypassword"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# create engine
@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(url=os.environ["DB_URL"], poolclass=NullPool)
    return engine


# create database
@pytest.fixture(scope="session")
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


# create session
@pytest.fixture
async def db_session(test_engine, setup_database):
    conn = await test_engine.connect()
    trann = await conn.begin()

    test_async_session = async_sessionmaker(
        bind=conn,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    session = test_async_session()

    try:
        yield session
    finally:
        await session.close()
        await trann.rollback()
        await conn.close()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# helper function
