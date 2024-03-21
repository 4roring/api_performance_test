import pytest
from httpx import AsyncClient
from typing import AsyncGenerator
from main import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
