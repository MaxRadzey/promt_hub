import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_ping(test_client: AsyncClient):
    response = await test_client.get("/technical/ping")

    assert response.status_code == 200
    assert response.json() == {
        "errors": [],
        "success": True,
        "result": {"status": "ok"},
    }


async def test_db(test_client: AsyncClient):
    response = await test_client.get("/technical/db")

    assert response.status_code == 200
    assert response.json() == {
        "errors": [],
        "success": True,
        "result": {"status": "ok", "database": "connected"},
    }
