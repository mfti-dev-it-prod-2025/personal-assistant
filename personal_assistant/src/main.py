import uvicorn
from fastapi import FastAPI

from personal_assistant.src.api.v1.auth.main import auth_router
from personal_assistant.src.api.v1.misc import router as misc_router
from personal_assistant.src.api.v1.user.user import user_router
from personal_assistant.src.api.v1.notes.note import router as note_router
from personal_assistant.src.configs.app import settings
from personal_assistant.src.exception_handlers import (
    user_already_exists_exception_handler,
)
from personal_assistant.src.exceptions import UserAlreadyExist

app = FastAPI(title="Personal assistant")

api_base_prefix = "/api/v1/"

app.include_router(misc_router, prefix=f"{api_base_prefix}misc", tags=["misc"])

app.include_router(auth_router, prefix=f"{api_base_prefix}auth", tags=["auth"])

app.include_router(user_router, prefix=f"{api_base_prefix}user", tags=["user"])

app.include_router(note_router, prefix=f"{api_base_prefix}notes", tags=["notes"])


app.add_exception_handler(
    exc_class_or_status_code=UserAlreadyExist,
    handler=user_already_exists_exception_handler,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.app_host,
        port=settings.app.app_port,
    )
