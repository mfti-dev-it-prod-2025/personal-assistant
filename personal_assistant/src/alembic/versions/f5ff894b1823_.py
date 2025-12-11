"""empty message

Revision ID: f5ff894b1823
Revises: 1f5f227a5a6b, 4aef60b10c63
Create Date: 2025-12-09 22:51:38.252156

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "f5ff894b1823"
down_revision: Union[str, Sequence[str], None] = ("1f5f227a5a6b", "4aef60b10c63")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
