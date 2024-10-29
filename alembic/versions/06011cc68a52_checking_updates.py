"""checking updates

Revision ID: 06011cc68a52
Revises: 059031210315
Create Date: 2024-10-29 11:12:39.658680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06011cc68a52'
down_revision: Union[str, None] = '059031210315'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'author')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
