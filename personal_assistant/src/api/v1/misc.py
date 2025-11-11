from fastapi import APIRouter

from personal_assistant.src.configs.app import settings
from personal_assistant.src.schemas.misc_schema import HelthCheckSchema

router = APIRouter()


@router.get("/health")
def health() -> HelthCheckSchema:
    return HelthCheckSchema(status="ok")