from personal_assistant.src.models.user import UserBase


class UserCreate(UserBase):
    password: str

class UserGet(UserBase):
    pass