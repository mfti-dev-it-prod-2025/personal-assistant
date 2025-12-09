from personal_assistant.src.models.budget import ExpenseTable

import random
from datetime import date
import pytest

@pytest.mark.asyncio
async def test_create_expense__then_expense_exists_in_db(postgres_connection, router_api_user):
    category_response = router_api_user.post(
        "/api/v1/expense_category/",
        json={"name": f"test_category_{random.randint(1, 10000)}", "description": "разное"}
    )
    category_response.raise_for_status()
    category_id = category_response.json()["id"]

    expense_data = {
        "name": "test_expense",
        "amount": random.randint(10, 1000),
        "currency": "RUB",
        "category_id": str(category_id),
        "tag": None,
        "shared": False,
        "expense_date": date.today().isoformat()
    }

    expense_response = router_api_user.post("/api/v1/expense/", json=expense_data)

    assert expense_response.status_code == 201, expense_response.text
    created_expense = expense_response.json()


    expense_in_db = await postgres_connection.get(ExpenseTable, created_expense["id"])
    assert expense_in_db is not None
    assert expense_in_db.user_id is not None
    assert expense_in_db.name == expense_data["name"]
    assert expense_in_db.amount == expense_data["amount"]


@pytest.mark.asyncio
async def test_list_expenses(router_api_user):
    response = router_api_user.get("/api/v1/expense/all")
    response.raise_for_status()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
