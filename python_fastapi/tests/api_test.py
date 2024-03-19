import pytest
from fastapi.testclient import TestClient
from main import app


def test_sync_client():
    test_value = 10
    client = TestClient(app)
    client.post(f"/sync/insert/{test_value}")
    response = client.get("/sync/select")
    response_data = response.json()
    data = response_data.get("data")
    assert test_value in data
