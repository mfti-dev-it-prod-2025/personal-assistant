import uvicorn
from fastapi import FastAPI

from api.v1.misc import router as misc_router
from personal_assistant.src.configs.app import settings

app = FastAPI(
    title="Personal assistant"
)


app.include_router(misc_router, prefix="/api/v1/misc", tags=["misc"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.app_host,
        port=settings.app.app_port,
    )
