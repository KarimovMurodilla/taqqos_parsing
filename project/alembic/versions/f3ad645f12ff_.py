"""empty message

Revision ID: f3ad645f12ff
Revises: 40a8dc67c6b0
Create Date: 2024-01-24 14:58:11.722971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3ad645f12ff'
down_revision: Union[str, None] = '40a8dc67c6b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('texnomart_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_texnomart_category_name'), 'texnomart_category', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_texnomart_category_name'), table_name='texnomart_category')
    op.drop_table('texnomart_category')
    # ### end Alembic commands ###