"""add last_checked to directors table

Revision ID: beaf829c5421
Revises:
Create Date: 2024-03-15 16:13:43.241363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "beaf829c5421"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "directors", sa.Column("last_checked", sa.DateTime, nullable=True)
    )


def downgrade() -> None:
    op.drop_column("directors", "last_checked")
