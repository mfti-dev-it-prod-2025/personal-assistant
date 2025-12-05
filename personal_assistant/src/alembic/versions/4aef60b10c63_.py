"""empty message

Revision ID: 4aef60b10c63
Revises: 04ad9941b0dc, f9a4cbe57362
Create Date: 2025-12-05 06:26:03.042848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '4aef60b10c63'
down_revision: Union[str, Sequence[str], None] = ('04ad9941b0dc', 'f9a4cbe57362')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
