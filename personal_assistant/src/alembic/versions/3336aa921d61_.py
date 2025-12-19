"""empty message

Revision ID: 3336aa921d61
Revises: 047f07327d97, 0c7cf0498bb2, 9687e09e1816
Create Date: 2025-12-19 09:30:10.830008

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '3336aa921d61'
down_revision: Union[str, Sequence[str], None] = ('047f07327d97', '0c7cf0498bb2', '9687e09e1816')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
