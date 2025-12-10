"""create expenses table

Revision ID: 047f07327d97
Revises: 9ccd99dcd2aa
Create Date: 2025-12-02 20:48:24.322307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '047f07327d97'
down_revision: Union[str, Sequence[str], None] = '9ccd99dcd2aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "expenses",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("currency", sa.String, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tag", sa.String, nullable=True),
        sa.Column("shared", sa.Boolean, nullable=False),
        sa.Column("expense_date", sa.Date, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("expenses")