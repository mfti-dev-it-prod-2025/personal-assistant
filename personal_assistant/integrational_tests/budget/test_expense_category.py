import random
import pytest

@pytest.mark.asyncio
async def test_create_expense_category(router_api_user):
    payload = {"name": f"category_{random.randint(1, 10000)}", "description": "тестовая категория"}
    response = router_api_user.post("/api/v1/expense_category/", json=payload)
    response.raise_for_status()

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data


@pytest.mark.asyncio
async def test_list_expense_categories(router_api_user, create_category):
    response = router_api_user.get("/api/v1/expense_category/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0