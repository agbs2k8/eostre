import os
import pytest
import asyncio
import pathlib
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from db import Base, get_session
from src.app import create_app


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DATABASE_URI": TEST_DATABASE_URL,
    })
    return app


@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine):
    """Creates a new DB session for a test."""
    async_session = sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture()
async def test_client(app, db_session, monkeypatch):
    # Patch the AsyncSessionLocal to return the test session
    monkeypatch.setattr("db.AsyncSessionLocal", lambda: db_session)

    async with app.test_app() as test_app:
        async with test_app.test_client() as client:
            yield client

from src.services.auth_manager import AuthManager


@pytest.fixture(scope="session")
def private_key():
    return pathlib.Path(os.getenv("PRIVATE_KEY_PATH", "private_key.pem")).read_text()


@pytest.fixture(scope="session")
def public_key():
    return pathlib.Path(os.getenv("PUBLIC_KEY_PATH", "public_key.pem")).read_text()


@pytest.fixture(scope="session")
def auth_manager(private_key, public_key):
    return AuthManager(
        private_key=private_key,
        public_key=public_key,
        key_algorithm="RS256",
        access_token_expiry=5,
        refresh_token_expiry=60
    )


# Standard Response fixtures
@pytest.fixture()
def ok_response():
    return "OK"