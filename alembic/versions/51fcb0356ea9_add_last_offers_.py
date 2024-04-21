"""add last_offers_*

Revision ID: 51fcb0356ea9
Revises: 6aeef95710d1
Create Date: 2024-03-24 17:15:41.627147

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "51fcb0356ea9"
down_revision: Union[str, None] = "6aeef95710d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("films", sa.Column("last_offers_checked", sa.DateTime, nullable=True))
    op.add_column("films", sa.Column("last_offers_updated", sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column("films", "last_offers_updated")
    op.drop_column("films", "last_offers_checked")
