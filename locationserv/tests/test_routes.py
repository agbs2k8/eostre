import pytest

@pytest.mark.anyio
async def test_liveness(async_client):
    """Test the /liveness endpoint."""
    response = await async_client.get("/liveness")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

@pytest.mark.anyio
async def test_readiness(async_client):
    """Test the /readiness endpoint."""
    response = await async_client.get("/readiness")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

@pytest.mark.anyio
async def test_list_locations_open(async_client):
    """Test the /locations endpoint (open)."""
    response = await async_client.get("/locations")
    assert response.status_code == 200
    assert "data" in response.json()