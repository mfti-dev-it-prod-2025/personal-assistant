from sqlalchemy import String, Float, Boolean, Date, text, ForeignKey, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from typing import Any

from personal_assistant.src.models.budget_base import Base, BaseModelMixin

class Expense(Base, BaseModelMixin):
    __tablename__ = "expenses"

    name = Column(String, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, server_default="RUB")

    # UUID foreign keys
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(PG_UUID(as_uuid=True), ForeignKey("expenses_categories.uuid"), nullable=False)

    tag = Column(String, nullable=True)
    shared = Column(Boolean, nullable=False, server_default=text("false"))
    date = Column(Date, nullable=False)

    # Связи
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    participants = relationship("ExpenseParticipant", back_populates="expense")

    def __repr__(self) -> str:
        return (
            f"Expense(uuid={self.uuid}, name={self.name}, amount={self.amount}, "
            f"date={self.date}, shared={self.shared})"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "amount": self.amount,
            "currency": self.currency,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "tag": self.tag,
            "shared": self.shared,
            "date": self.date,
            "created_at": self.create_at,
            "updated_at": self.update_at,
        }