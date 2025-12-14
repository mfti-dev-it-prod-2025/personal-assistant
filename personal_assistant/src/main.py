# personal_assistant/src/main.py
import uvicorn
from fastapi import FastAPI

from personal_assistant.src.api.v1.auth.main import auth_router
from personal_assistant.src.api.v1.expense.expense import expense_router
from personal_assistant.src.api.v1.misc import router as misc_router
from personal_assistant.src.api.v1.events.routes import router as events_router
from personal_assistant.src.api.v1.notes.note import router as note_router
from personal_assistant.src.api.v1.tasks.endpoints import router as tasks_router
from personal_assistant.src.api.v1.user.user import user_router
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

app.include_router(events_router, prefix=f"{api_base_prefix}events", tags=["events"])

app.include_router(note_router, prefix=f"{api_base_prefix}notes", tags=["notes"])

app.include_router(expense_router, prefix=f"{api_base_prefix}expense", tags=["expense"])


app.include_router(tasks_router, prefix=f"{api_base_prefix}tasks", tags=["tasks"])

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
