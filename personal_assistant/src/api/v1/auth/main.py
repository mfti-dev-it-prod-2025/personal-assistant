from fastapi import APIRouter

from personal_assistant.src.api.v1.auth.user import user_router

auth_router = APIRouter()

auth_router.include_router(user_router, prefix="/user")

