"""agregar url a musica

Revision ID: 67a007058a0f
Revises: 
Create Date: 2026-09-19 14:13:03.918147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67a007058a0f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('musica', sa.Column('url', sa.String(), nullable=True))
    op.create_unique_constraint('uq_musica_url', 'musica', ['url'])


def downgrade() -> None:
    op.drop_constraint('uq_musica_url', 'musica', type_='unique')
    op.drop_column('musica', 'url')
