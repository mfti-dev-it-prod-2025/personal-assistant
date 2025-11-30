from personal_assistant.src.repositories.note import NoteRepository
from personal_assistant.src.models.note import NoteCreate, NoteUpdate, NoteRead, NoteReadUpdate
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

class NoteService:
    def __init__(self, session: AsyncSession):
        self.note_repo = NoteRepository(session)

    async def create_note(self, note_data: NoteCreate, user_id: uuid.UUID) -> NoteRead:
        db_note = await self.note_repo.create_note(note_data, user_id)
        return NoteRead.model_validate(db_note)

    async def get_note(self, note_id: uuid.UUID, user_id: uuid.UUID) -> Optional[NoteRead]:
        db_note = await self.note_repo.get_note_by_id(note_id, user_id)
        if db_note:
            return NoteRead.model_validate(db_note)
        return None

    async def get_notes(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[NoteRead]:
        db_notes = await self.note_repo.get_notes_by_user(user_id, skip, limit)
        return [NoteRead.model_validate(note) for note in db_notes]

    async def update_note(self, note_id: uuid.UUID, user_id: uuid.UUID, note_data: NoteUpdate) -> Optional[NoteReadUpdate]:
        db_note = await self.note_repo.update_note(note_id, user_id, note_data)
        if db_note:
             return NoteReadUpdate.model_validate(db_note)
        return None

    async def delete_note(self, note_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        return await self.note_repo.delete_note(note_id, user_id)
