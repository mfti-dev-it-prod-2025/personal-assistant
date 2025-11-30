"""create expenses table

Revision ID: cf10c15fd556
Revises: 9ccd99dcd2aa
Create Date: 2025-11-30 20:22:23.389010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from personal_assistant.src.models.budget import ExpenseTable


# revision identifiers, used by Alembic.
revision: str = 'cf10c15fd556'
down_revision: Union[str, Sequence[str], None] = '9ccd99dcd2aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "expenses",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("currency", sa.String, nullable=False),
        sa.Column("user_id", sa.String, nullable=False),
        sa.Column("category_id", sa.String, nullable=True),
        sa.Column("tag", sa.String, nullable=True),
        sa.Column("shared", sa.Boolean, nullable=False),
        sa.Column("expense_date", sa.Date, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("expenses")