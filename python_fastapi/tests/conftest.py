import pytest
from httpx import AsyncClient
from typing import AsyncGenerator
from main import app
from table import Base
from db import db


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def setup_test_init():
    Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(db.engine)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
