import pytest

from personal_assistant.integrational_tests.utils import random_email


@pytest.mark.asyncio
async def test_create_user__then_authorise(postgres_connection, router_api):
    email = random_email()
    response = router_api.post("/api/v1/auth/user/", json={"name": "test_user",
                                                           "email": email,
                                                           "password": "test"})

    response.raise_for_status()

    response = router_api.post("/api/v1/auth/token",
                               headers={"Content-Type": "application/x-www-form-urlencoded",
                                        "accept": "application/json"},
                               data={
                                    "grant_type": "password",
                                    "username": email,
                                    "password": "test",
                                },
                               )
    response.raise_for_status()
