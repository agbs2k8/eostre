import pytest


@pytest.mark.asyncio
async def test_api_not_found(test_client):
    response = await test_client.get("/api/v1/doesNotExist")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_api_not_allowed(test_client):
    response = await test_client.post("/api/v1/liveness")
    assert response.status_code == 405


@pytest.mark.asyncio
async def test_api_live(test_client, ok_response):
    response = await test_client.get("/api/v1/liveness")
    assert response.status_code == 200
    resp_data = await response.get_json()
    assert resp_data.get("message") == ok_response


@pytest.mark.asyncio
async def test_api_ready(test_client, ok_response):
    response = await test_client.get("/api/v1/readiness")
    assert response.status_code == 200
    resp_data = await response.get_json()
    assert resp_data.get("message") == ok_response


# @pytest.mark.asyncio
# async def test_secure_route_with_valid_token(test_client, auth_manager):
#     token = auth_manager.generate_token("user123", roles=["user"])
#     response = await test_client.get("/secure", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     json_data = await response.get_json()
#     assert json_data["message"] == "Access granted"

# @pytest.mark.asyncio
# async def test_login_success(test_client):
#     response = await test_client.post("/login", json={"username": "bob", "password": "secret"})
#     assert response.status_code == 200