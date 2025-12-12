from pydantic import BaseModel

from personal_assistant.src.schemas.auth.user import UserGet


class UserListResponse(BaseModel):
    result: list[UserGet]
    limit: int
    offset: int
    total: int