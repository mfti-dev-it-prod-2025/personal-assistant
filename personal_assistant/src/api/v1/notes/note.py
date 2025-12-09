from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid
from ....models.database_session import get_session
from ....services.note_service import NoteService
from ....schemas.note import NoteCreate, NoteUpdate, NoteRead, NoteReadUpdate
from ...dependencies import get_current_user_dependency as get_current_user, get_current_user_dependency, \
    DbSessionDepends
from ....models.user import UserTable

router = APIRouter(prefix="", tags=["notes"])

def get_note_service(session: DbSessionDepends):
    return NoteService(session)

note_service_dependency = Annotated[NoteService, Depends(get_note_service)]

@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["note:create"])
    ],
    note_service: note_service_dependency
):
    return await note_service.create_note(note_data, current_user.id)


@router.get("/{note_id}", response_model=NoteRead)
async def read_note(
    note_id: uuid.UUID,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["note:read"])
    ],
    note_service: note_service_dependency
):
    note = await note_service.get_note(note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена")
    return note

@router.get("/", response_model=list[NoteRead])
async def read_notes(
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["note:read"])
    ],
    note_service: note_service_dependency,
    skip: int = 0,
    limit: int = 1000,
) -> list[NoteRead]:
    return await note_service.get_notes(current_user.id, skip=skip, limit=limit)

@router.put("/{note_id}")
async def update_note(
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["note:update"])
    ],
    note_id: uuid.UUID,
    note_data: NoteUpdate,
    note_service: note_service_dependency,
) -> NoteReadUpdate:
    updated_note = await note_service.update_note(note_id, current_user.id, note_data)
    if not updated_note:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена")
    return updated_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["note:delete"])
    ],
    note_id: uuid.UUID,
    note_service: note_service_dependency,
):
    success = await note_service.delete_note(note_id, current_user.id)
    if not success:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена")
    return
