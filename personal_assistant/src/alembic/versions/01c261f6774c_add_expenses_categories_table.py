"""add categories table

Revision ID: 01c261f6774c
Revises: cf10c15fd556
Create Date: 2025-11-30 20:58:28.489821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '01c261f6774c'
down_revision: Union[str, Sequence[str], None] = 'cf10c15fd556'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'expenses_categories',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('name', sa.String(100), unique=True, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()'))
    )



def downgrade():
    op.drop_table('categories')