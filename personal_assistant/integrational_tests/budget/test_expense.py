import pytest
import random
from sqlmodel import select
from personal_assistant.src.models.budget import ExpenseTable
from datetime import date

@pytest.mark.asyncio
async def test_create_expense__then_expense_exist_in_db(postgres_connection, router_api):
    # - Создаем пользователя через API
    user_response = router_api.post(
        "/api/v1/user/",
        json={
            "name": "test_user",
            "email": f"test{random.randint(1,10000)}@example.com",
            "password": "test"
        }
    )
    user_response.raise_for_status()
    user_id = user_response.json()["id"]

    # - Создаем категорию через API
    category_response = router_api.post(
        "/api/v1/expense_category/",
        json={"name": f"test_category_{random.randint(1,10000)}", "description":"разное"}
    )
    category_response.raise_for_status()
    category_id = category_response.json()["id"]

    # - Создаем расход через API
    expense_data = {
        "name": "test_expense",
        "amount": random.randint(10, 1000),
        "currency": "RUB",
        "user_id": str(user_id),
        "category_id": str(category_id),
        "tag": None,
        "shared": False,
        "expense_date": date.today().isoformat()
    }
    expense_response = router_api.post("/api/v1/expense/", json=expense_data)
    expense_response.raise_for_status()
    expense_json = expense_response.json()

    # - Проверяем, что запись есть в БД
    db_result = await postgres_connection.exec(
        select(ExpenseTable).where(ExpenseTable.id == expense_json["id"])
    )
    db_result = db_result.one()

    assert str(db_result.id) == expense_json["id"]
    assert db_result.name == expense_json["name"]
    assert db_result.amount == expense_json["amount"]
    assert str(db_result.user_id) == expense_json["user_id"]
    assert str(db_result.category_id) == expense_json["category_id"]