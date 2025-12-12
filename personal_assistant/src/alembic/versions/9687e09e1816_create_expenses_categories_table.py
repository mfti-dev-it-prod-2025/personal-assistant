"""create expenses_categories table

Revision ID: 9687e09e1816
Revises: 047f07327d97
Create Date: 2025-12-02 20:51:48.408684

"""

from typing import Sequence, Union
from sqlalchemy.dialects import postgresql

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9687e09e1816"
down_revision: Union[str, Sequence[str], None] = "9ccd99dcd2aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "expenses_categories",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column(
            "created_at", sa.DateTime, nullable=True, server_default=sa.text("now()")
        ),
        sa.Column(
            "updated_at", sa.DateTime, nullable=True, server_default=sa.text("now()")
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.UniqueConstraint("name", "user_id", name="expenses_categories_name_user_key"),
        sa.ForeignKeyConstraint(
            ["user_id"], ["usertable.id"], ondelete="CASCADE"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("expenses_categories")
