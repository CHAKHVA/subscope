from httpx import AsyncClient
import pytest

from main import app as fastapi_app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db_host": None}
