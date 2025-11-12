from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from personal_assistant.src.exceptions import UserAlreadyExist


async def user_already_exists_exception_handler(
        request: Request, exc: UserAlreadyExist
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Пользователь с таким email уже существует"},
    )