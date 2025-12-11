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
async def test_get_category_by_id(router_api_user, router_api_category):
    resp = router_api_user.get(
        f"/api/v1/expense_category/?id={router_api_category['id']}"
    )

    assert resp.status_code == 200
    assert resp.json()["name"] == router_api_category["name"]


@pytest.mark.asyncio
async def test_get_category_by_name(router_api_user, router_api_category):
    resp = router_api_user.get(
        f"/api/v1/expense_category/?name={router_api_category['name']}"
    )

    assert resp.status_code == 200
    assert resp.json()["id"] == router_api_category["id"]


@pytest.mark.asyncio
async def test_get_all_categories(router_api_user, router_api_category):
    resp = router_api_user.get("/api/v1/expense_category/all")

    assert resp.status_code == 200
    categories = resp.json()
    assert isinstance(categories, list)
    assert len(categories) > 0
    assert any(cat["id"] == router_api_category["id"] for cat in categories)


def test_update_category(router_api_user, router_api_category):
    payload = {"description": "Обновленное описание"}

    resp = router_api_user.put(
        f"/api/v1/expense_category/{router_api_category['name']}",
        json=payload,
    )

    resp.raise_for_status()
    data = resp.json()

    assert resp.status_code == 200
    assert data["description"] == "Обновленное описание"


@pytest.mark.asyncio
async def test_delete_category(router_api_user, router_api_category):
    resp = router_api_user.delete(
        f"/api/v1/expense_category/{router_api_category['name']}"
    )

    assert resp.status_code == 204


