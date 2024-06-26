"""Delete column number of users

Revision ID: 93ef6603f8de
Revises: fc92c82621fa
Create Date: 2024-04-23 22:44:42.097045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93ef6603f8de'
down_revision: Union[str, None] = 'fc92c82621fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('number', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
