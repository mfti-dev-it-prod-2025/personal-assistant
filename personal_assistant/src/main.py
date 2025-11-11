import uvicorn
from fastapi import FastAPI

from personal_assistant.src.api.v1.auth.main import auth_router
from personal_assistant.src.api.v1.misc import router as misc_router
from personal_assistant.src.configs.app import settings

app = FastAPI(title="Personal assistant")

api_base_prefix = "/api/v1/"

app.include_router(misc_router, prefix=f"{api_base_prefix}misc", tags=["misc"])

app.include_router(auth_router, prefix=f"{api_base_prefix}auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.app_host,
        port=settings.app.app_port,
    )
