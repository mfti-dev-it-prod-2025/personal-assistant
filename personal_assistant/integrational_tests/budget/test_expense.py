import pytest

@pytest.mark.asyncio
async def test_create_expense(router_api_user, router_api_category):
    payload = {
        "name": "Coffee",
        "amount": 50.0,
        "currency": "RUB",
        "category_id": router_api_category["id"],
        "shared": False,
        "expense_date": date.today().isoformat(),
    }

    resp = router_api_user.post("/api/v1/expense", json=payload)
    assert resp.status_code == 201

    body = resp.json()
    assert body["name"] == "Coffee"
    assert body["amount"] == 50.0
    assert body["currency"] == "RUB"
    assert body["category_id"] == router_api_category["id"]
    assert body["shared"] is False
    assert "id" in body


@pytest.mark.asyncio
async def test_get_expense_by_id(router_api_user, api_router_expense):
    resp = router_api_user.get(f"/api/v1/expense/?id={api_router_expense['id']}")
    assert resp.status_code == 200

    body = resp.json()
    assert body["id"] == api_router_expense["id"]
    assert body["name"] == api_router_expense["name"]
    assert body["amount"] == api_router_expense["amount"]

@pytest.mark.asyncio
async def test_get_expense_by_name_(router_api_user, api_router_expense):

    resp = router_api_user.get(f"/api/v1/expense/?name={api_router_expense['name']}")

    assert resp.status_code == 200

    body = resp.json()
    assert body["id"] == api_router_expense["id"]
    assert body["name"] == api_router_expense["name"]
    assert body["amount"] == api_router_expense["amount"]


import pytest
from datetime import date

@pytest.mark.asyncio
async def test_get_all_expenses(router_api_user, api_router_expense, router_api_category):
    resp = router_api_user.get("/api/v1/expense/all")
    assert resp.status_code == 200
    expenses = resp.json()
    assert isinstance(expenses, list)
    assert any(exp["id"] == api_router_expense["id"] for exp in expenses)

    resp_category = router_api_user.get(
        f"/api/v1/expense_category/?name={router_api_category['name']}"
    )
    category_name = resp_category.json()['name']

    resp_category = router_api_user.get(f"/api/v1/expense/all?category_name={category_name}")
    assert resp_category.status_code == 200
    expenses_category = resp_category.json()
    assert all(exp["category_id"] == api_router_expense["category_id"] for exp in expenses_category)

    start_date = api_router_expense["expense_date"]
    end_date = api_router_expense["expense_date"]
    resp_date = router_api_user.get(f"/api/v1/expense/all?start_date={start_date}&end_date={end_date}")
    assert resp_date.status_code == 200
    expenses_date = resp_date.json()
    assert all(exp["expense_date"] == start_date for exp in expenses_date)


@pytest.mark.asyncio
async def test_update_expense(router_api_user, api_router_expense):
    payload = {"amount": 120.0}

    resp = router_api_user.put(
        f"/api/v1/expense/{api_router_expense['id']}",
        json=payload,
    )
    assert resp.status_code == 200

    body = resp.json()
    assert body["id"] == api_router_expense["id"]
    assert body["amount"] == 120.0
    assert body["name"] == api_router_expense["name"]
    assert body["currency"] == api_router_expense["currency"]
    assert body["category_id"] == api_router_expense["category_id"]
    assert body["shared"] == api_router_expense["shared"]


@pytest.mark.asyncio
async def test_delete_expense(router_api_user, api_router_expense):
    resp = router_api_user.delete(f"/api/v1/expense/{api_router_expense['id']}")
    assert resp.status_code == 204

    get_resp = router_api_user.get(f"/api/v1/expense/?id={api_router_expense['id']}")
    assert get_resp.status_code == 400 or get_resp.status_code == 404