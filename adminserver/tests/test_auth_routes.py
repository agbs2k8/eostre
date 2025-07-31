import pytest
import jwt
from models.models import User

@pytest.mark.asyncio
async def test_login_success(test_client, db_session, monkeypatch):
    async def mock_login(username, password, session):
        class FakeUser:
            id = 1
            name = "testuser"
            type = "admin"
        return FakeUser()

    monkeypatch.setattr(User, "login", mock_login)

    resp = await test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })

    assert resp.status_code == 200
    data = await resp.get_json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_refresh_token_success(test_client, auth_manager):
    payload = {
        "sub": "1",
        "username": "testuser",
        "type": "refresh"
    }
    token = auth_manager.create_refresh_token(payload)

    resp = await test_client.post("/auth/refresh", json={"refresh_token": token})
    assert resp.status_code == 200
    data = await resp.get_json()
    assert "access_token" in data

@pytest.mark.asyncio
async def test_refresh_token_invalid(test_client):
    resp = await test_client.post("/auth/refresh", json={"refresh_token": "invalid.token"})
    assert resp.status_code == 401
    data = await resp.get_json()
    assert "error" in data
