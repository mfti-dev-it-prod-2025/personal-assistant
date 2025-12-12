import pytest
from datetime import date


@pytest.mark.asyncio
async def test_create_expense(router_api_user, router_api_category):
    payload = {
        "name": "Кофе",
        "amount": 50.0,
        "currency": "RUB",
        "category_id": router_api_category["id"],
        "shared": False,
        "expense_date": date.today().isoformat(),
    }

    resp = router_api_user.post("/api/v1/expense/", json=payload)
    assert resp.status_code == 201

    body = resp.json()
    assert body["name"] == "Кофе"
    assert body["amount"] == 50.0
    assert body["currency"] == "RUB"
    assert body["category_id"] == router_api_category["id"]
    assert body["shared"] is False
    assert "id" in body
    assert "user_id" in body


@pytest.mark.asyncio
async def test_get_expense_by_id(router_api_user, router_api_expense):
    resp = router_api_user.get(f"/api/v1/expense/?id={router_api_expense['id']}")
    assert resp.status_code == 200

    body = resp.json()
    assert body["id"] == router_api_expense["id"]
    assert "user_id" in body
    assert body["name"] == router_api_expense["name"]
    assert body["amount"] == router_api_expense["amount"]


@pytest.mark.asyncio
async def test_get_expense_by_name(router_api_user, router_api_expense):
    resp = router_api_user.get(f"/api/v1/expense/?name={router_api_expense['name']}")
    assert resp.status_code == 200

    body = resp.json()
    assert body["id"] == router_api_expense["id"]
    assert "user_id" in body
    assert body["name"] == router_api_expense["name"]
    assert body["amount"] == router_api_expense["amount"]


@pytest.mark.asyncio
async def test_get_all_expenses(router_api_user, router_api_expense, router_api_category):
    resp = router_api_user.get("/api/v1/expense/all")
    assert resp.status_code == 200
    expenses = resp.json()
    assert isinstance(expenses, list)
    assert any(exp["id"] == router_api_expense["id"] for exp in expenses)
    assert all("user_id" in exp for exp in expenses)

    resp_category = router_api_user.get(
        f"/api/v1/expense_category/?name={router_api_category['name']}"
    )
    category_name = resp_category.json()['name']

    resp_category = router_api_user.get(f"/api/v1/expense/all?category_name={category_name}")
    assert resp_category.status_code == 200
    expenses_category = resp_category.json()
    assert all(exp["category_id"] == router_api_expense["category_id"] for exp in expenses_category)
    assert all("user_id" in exp for exp in expenses_category)

    start_date = router_api_expense["expense_date"]
    end_date = router_api_expense["expense_date"]
    resp_date = router_api_user.get(f"/api/v1/expense/all?start_date={start_date}&end_date={end_date}")
    assert resp_date.status_code == 200
    expenses_date = resp_date.json()
    assert all(exp["expense_date"] == start_date for exp in expenses_date)
    assert all("user_id" in exp for exp in expenses_date)


@pytest.mark.asyncio
async def test_update_expense(router_api_user, router_api_expense):
    payload = {"amount": 120.0}

    resp = router_api_user.put(
        f"/api/v1/expense/{router_api_expense['id']}",
        json=payload,
    )
    assert resp.status_code == 200

    body = resp.json()
    assert body["id"] == router_api_expense["id"]
    assert body["amount"] == 120.0
    assert body["name"] == router_api_expense["name"]
    assert body["currency"] == router_api_expense["currency"]
    assert body["category_id"] == router_api_expense["category_id"]
    assert body["shared"] == router_api_expense["shared"]
    assert "user_id" in body


@pytest.mark.asyncio
async def test_delete_expense(router_api_user, router_api_expense):
    resp = router_api_user.delete(f"/api/v1/expense/{router_api_expense['id']}")
    assert resp.status_code == 204

    get_resp = router_api_user.get(f"/api/v1/expense/?id={router_api_expense['id']}")
    assert get_resp.status_code in [400, 404]