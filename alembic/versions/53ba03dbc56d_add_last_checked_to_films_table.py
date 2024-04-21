"""add last_checked to films table

Revision ID: 53ba03dbc56d
Revises: beaf829c5421
Create Date: 2024-03-15 18:32:48.974996

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "53ba03dbc56d"
down_revision: Union[str, None] = "beaf829c5421"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("films", sa.Column("last_checked", sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column("films", "last_checked")
