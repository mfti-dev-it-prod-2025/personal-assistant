from fastapi import APIRouter

from personal_assistant.src.api.dependencies import DbSessionDepends
from personal_assistant.src.repositories.user import UserRepository
from personal_assistant.src.schemas.auth.user import UserGet, UserCreate

user_router = APIRouter()

@user_router.get("/")
async def get_user(db_session: DbSessionDepends) -> list[UserGet]:
    return await UserRepository(db_session=db_session).get_all_users()

@user_router.post("/")
async def create_user(user: UserCreate, db_session: DbSessionDepends) -> UserGet:
    return await UserRepository(db_session=db_session).create_user(user)