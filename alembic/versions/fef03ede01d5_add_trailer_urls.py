"""add-trailer-urls

Revision ID: fef03ede01d5
Revises: 51fcb0356ea9
Create Date: 2024-05-19 12:54:59.650943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fef03ede01d5'
down_revision: Union[str, None] = '51fcb0356ea9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('films', sa.Column('trailer_url', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('films', 'trailer_url')
