import pytest
import jwt


def test_create_access_token(auth_manager, public_key):
    payload = {"sub": "123", "username": "testuser", "type": "admin", "grants": ["read", "write"]}
    token = auth_manager.create_access_token(payload)
    decoded = jwt.decode(token, public_key, algorithms=["RS256"])
    assert decoded["sub"] == "123"
    assert decoded["username"] == "testuser"
    assert decoded["type"] == "access"
    assert decoded["grants"] == ["read", "write"]
    assert "exp" in decoded

def test_create_refresh_token(auth_manager, public_key):
    payload = {"sub": "123", "username": "testuser", "type": "admin"}
    token = auth_manager.create_refresh_token(payload)
    decoded = jwt.decode(token, public_key, algorithms=["RS256"])
    assert decoded["type"] == "refresh"

def test_verify_token(auth_manager):
    payload = {"sub": "123", "username": "testuser", "type": "admin"}
    token = auth_manager.create_access_token(payload)
    decoded = auth_manager.verify_token(token)
    assert decoded["sub"] == "123"
