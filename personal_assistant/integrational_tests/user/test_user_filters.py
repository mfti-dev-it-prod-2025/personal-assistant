import pytest

from personal_assistant.integrational_tests.utils import random_email, random_string


def _create_user(client, email: str, name: str | None = None):
    if name is None:
        # Valid Cyrillic name per regex ^[А-Я][А-я]+
        name = "Тестовый"
    response = client.post(
        "/api/v1/user/",
        json={"name": name, "email": email, "password": "test"},
    )
    response.raise_for_status()
    return response.json()


@pytest.mark.asyncio
async def test_filter_by_email_exact(router_api_admin):
    user1 = _create_user(router_api_admin, email=random_email())
    _create_user(router_api_admin, email=random_email())

    r = router_api_admin.get(f"/api/v1/user/?email={user1['email']}")
    r.raise_for_status()
    data = r.json()

    assert len(data) == 1
    assert data[0]["id"] == user1["id"]
    assert data[0]["email"] == user1["email"]


@pytest.mark.asyncio
async def test_filter_by_email_contains(router_api_admin):
    marker = f"filterx_{random_string()}"
    q = marker.lower()
    emails = [f"{marker}_a@{random_string()}.ru", f"{marker}_b@{random_string()}.ru"]

    for em in emails:
        _create_user(router_api_admin, email=em)

    r = router_api_admin.get(f"/api/v1/user/?email__contains={q}")
    r.raise_for_status()
    data = r.json()

    assert len(data) == 2
    assert all(q in u["email"] for u in data)


@pytest.mark.asyncio
async def test_filter_by_name_contains(router_api_admin):
    marker = f"namefilter_{random_string()}"
    # Use Cyrillic-only names to satisfy name regex
    names = [f"Тест{marker}А", f"Тест{marker}Б"]
    for nm in names:
        _create_user(router_api_admin, name=nm, email=random_email())

    r = router_api_admin.get(f"/api/v1/user/?name__contains={marker}")
    r.raise_for_status()
    data = r.json()

    assert len(data) == 2
    assert all(marker in u["name"] for u in data)


@pytest.mark.asyncio
async def test_filter_by_role_with_contains(router_api_admin):
    marker = f"rolemark_{random_string()}"
    q = marker.lower()
    # Create users with role=user (default)
    for _ in range(2):
        _create_user(
            router_api_admin,
            email=f"{marker}_{random_string()}@{random_string()}.ru",
        )

    # role=user should return the two created; role=administrator should return none for this marker
    r_user = router_api_admin.get(
        f"/api/v1/user/?email__contains={q}&role=user"
    )
    r_user.raise_for_status()
    data_user = r_user.json()
    assert len(data_user) == 2

    r_admin = router_api_admin.get(
        f"/api/v1/user/?email__contains={q}&role=administrator"
    )
    r_admin.raise_for_status()
    data_admin = r_admin.json()
    assert data_admin == []


@pytest.mark.asyncio
async def test_filter_with_pagination_limit_offset(router_api_admin):
    marker = f"pagin_{random_string()}"
    q = marker.lower()
    for _ in range(3):
        _create_user(
            router_api_admin,
            email=f"{marker}_{random_string()}@{random_string()}.ru",
        )

    r_limit2 = router_api_admin.get(
        f"/api/v1/user/?email__contains={q}&limit=2"
    )
    r_limit2.raise_for_status()
    data_limit2 = r_limit2.json()
    assert len(data_limit2) == 2
    assert all(q in u["email"] for u in data_limit2)

    r_offset2 = router_api_admin.get(
        f"/api/v1/user/?email__contains={q}&limit=5&offset=2"
    )
    r_offset2.raise_for_status()
    data_offset2 = r_offset2.json()
    # We created 3, so after skipping 2 there should be 1 left
    assert len(data_offset2) == 1
    assert q in data_offset2[0]["email"]
