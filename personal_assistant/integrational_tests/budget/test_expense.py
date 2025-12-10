from personal_assistant.src.models.budget import ExpenseTable

import random
from datetime import date
import pytest


import pytest

@pytest.mark.asyncio
async def test_create_expense(router_api_user, test_category):
    payload = {
        "name": "Coffee",
        "amount": 50.0,
        "currency": "RUB",
        "category_id": test_category["id"],
        "shared": False,
    }

    resp = router_api_user.post("/api/v1/expenses/", json=payload)

    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Coffee"
    assert body["amount"] == 50.0
    assert body["category_id"] == test_category["id"]


@pytest.mark.asyncio
async def test_get_expense(router_api_user, test_expense):
    resp = router_api_user.get(f"/api/v1/expenses/{test_expense['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Groceries"


@pytest.mark.asyncio
async def test_get_all_expenses(router_api_user):
    resp = router_api_user.get("/api/v1/expenses/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_update_expense(router_api_user, test_expense):
    payload = {"amount": 120.0}

    resp = router_api_user.put(
        f"/api/v1/expenses/{test_expense['id']}",
        json=payload,
    )

    assert resp.status_code == 200
    assert resp.json()["amount"] == 120.0


@pytest.mark.asyncio
async def test_delete_expense(router_api_user, test_expense):
    resp = router_api_user.delete(f"/api/v1/expenses/{test_expense['id']}")
    assert resp.status_code == 204


#
# @pytest.mark.asyncio
# async def test_create_expense__then_expense_exists_in_db(postgres_connection, router_api_user):
#     category_response = router_api_user.post(
#         "/api/v1/expense_category/",
#         json={"name": f"test_category_{random.randint(1, 10000)}", "description": "разное"}
#     )
#     category_response.raise_for_status()
#     category_id = category_response.json()["id"]
#
#     expense_data = {
#         "name": "test_expense",
#         "amount": random.randint(10, 1000),
#         "currency": "RUB",
#         "category_id": str(category_id),
#         "tag": None,
#         "shared": False,
#         "expense_date": date.today().isoformat()
#     }
#
#     expense_response = router_api_user.post("/api/v1/expense/", json=expense_data)
#
#     assert expense_response.status_code == 201, expense_response.text
#     created_expense = expense_response.json()
#
#
#     expense_in_db = await postgres_connection.get(ExpenseTable, created_expense["id"])
#     assert expense_in_db is not None
#     assert expense_in_db.user_id is not None
#     assert expense_in_db.name == expense_data["name"]
#     assert expense_in_db.amount == expense_data["amount"]
#
#
# @pytest.mark.asyncio
# async def test_list_expenses(router_api_user):
#     response = router_api_user.get("/api/v1/expense/all")
#     response.raise_for_status()
#
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
