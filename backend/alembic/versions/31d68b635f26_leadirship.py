"""Leadirship

Revision ID: 31d68b635f26
Revises: efa749086bd7
Create Date: 2024-05-27 19:05:18.134711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31d68b635f26'
down_revision: Union[str, None] = 'efa749086bd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activeUsers', sa.Column('is_leader', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activeUsers', 'is_leader')
    # ### end Alembic commands ###