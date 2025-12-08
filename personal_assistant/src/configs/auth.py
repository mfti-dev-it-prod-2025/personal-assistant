from fastapi.security import OAuth2PasswordBearer

SCOPES: dict[str, str] = {
    "users:read": "Чтение списка пользователей и их данных",
    "users:write": "Создание и изменение пользователей",
    "me:read": "Чтение собственных данных пользователя",
    "tasks:read": "Чтение задач",
    "tasks:write": "Создание и изменение задач",
}

ROLES_TO_SCOPES = {
    "administrator": list(SCOPES.keys()),
    "user": ["me:read", "tasks:read", "tasks:write"],
    "note:create": "Создание пользователем заметки",
    "note:update": "Обновление заметки пользователем",
    "note:delete": "Удаление заметки пользователем",
    "tasks:read": "Чтение задач",
    "tasks:write": "Создание и изменение задач",
}
ROLES_TO_SCOPES = {
    "administrator": list(SCOPES.keys()),
    "user": ["me:read", "note:create", "note:update", "note:delete", "note:read","tasks:read", "tasks:write"],

}
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    scopes=SCOPES,
)
