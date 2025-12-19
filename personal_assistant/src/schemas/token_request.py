from sqlmodel import SQLModel


class TokenRequest(SQLModel):
    email: str
    password: str
