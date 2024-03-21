import pytest
from fastapi.testclient import TestClient
from main import app
from httpx import AsyncClient


# def test_sync_client():
#     test_value = "10"
#     client = TestClient(app)
#     client.post(f"/sync/insert/{test_value}")
#     response = client.get("/sync/select")
#     response_data = response.json()
#     data = response_data.get("data")
#     assert test_value == data[0]["data"]


@pytest.mark.anyio
async def test_async_client(async_client: AsyncClient):
    test_value = 10
    await async_client.post(f"/async/insert/{test_value}")
    response = await async_client.get("/async/select")
    response_data = response.json()
    data = response_data.get("data")
    assert str(test_value) == data[0]["data"]
