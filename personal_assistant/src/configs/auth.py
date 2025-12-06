from fastapi.security import OAuth2PasswordBearer

SCOPES: dict[str, str] = {
    "users:read": "Чтение списка пользователей и их данных",
    "users:write": "Создание и изменение пользователей",
    "me:read": "Чтение собственных данных пользователя",
    "tasks:read": "Чтение задач",  # ДОБАВЛЕНО
    "tasks:write": "Создание и изменение задач",  # ДОБАВЛЕНО
}
ROLES_TO_SCOPES = {
    "administrator": list(SCOPES.keys()),
    "user": ["me:read", "tasks:read", "tasks:write"],  # ДОБАВЛЕНЫ SCOPES ДЛЯ ЗАДАЧ
}
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    scopes=SCOPES,
)