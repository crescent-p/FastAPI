"""adding column to posts table content

Revision ID: a029e3f94d89
Revises: 32bda19edfdf
Create Date: 2024-10-20 22:50:50.667468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a029e3f94d89'
down_revision: Union[str, None] = '32bda19edfdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
