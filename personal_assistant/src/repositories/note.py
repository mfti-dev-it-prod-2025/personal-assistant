from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, and_
from typing import List, Optional
from datetime import datetime, timezone
import uuid
from ..models.note import Note
from ..schemas.note import NoteCreate, NoteUpdate


class NoteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_note(self, note_data: NoteCreate, user_id: uuid.UUID) -> Note:
        db_note = Note.model_validate(note_data, update={"user_id": user_id})
        self.session.add(db_note)
        await self.session.commit()
        await self.session.refresh(db_note)
        return db_note

    async def get_note_by_id(
        self, note_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Note]:
        statement = select(Note).where(
            and_(Note.id == note_id, Note.user_id == user_id)
        )
        result = await self.session.exec(statement)
        return result.first()

    async def get_notes_by_user(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 1000
    ) -> List[Note]:
        statement = (
            select(Note).where(Note.user_id == user_id).offset(skip).limit(limit)
        )
        result = await self.session.exec(statement)
        return result.all()

    async def update_note(
        self, note_id: uuid.UUID, user_id: uuid.UUID, note_data: NoteUpdate
    ) -> Optional[Note]:
        db_note = await self.get_note_by_id(note_id, user_id)
        if not db_note:
            return None

        update_data = note_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_note, field, value)

        self.session.add(db_note)
        await self.session.commit()
        await self.session.refresh(db_note)
        return db_note

    async def delete_note(self, note_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        db_note = await self.get_note_by_id(note_id, user_id)
        if not db_note:
            return False
        await self.session.delete(db_note)
        await self.session.commit()
        return True
