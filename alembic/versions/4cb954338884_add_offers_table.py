"""add offers table

Revision ID: 4cb954338884
Revises: 53ba03dbc56d
Create Date: 2024-03-15 19:19:53.889208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4cb954338884"
down_revision: Union[str, None] = "53ba03dbc56d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "offers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), unique=True),
    )
    op.create_table(
        "film_offer_association_table",
        sa.Column("film_id", sa.Integer, sa.ForeignKey("films.id")),
        sa.Column("offer_id", sa.Integer, sa.ForeignKey("offers.id")),
    )


def downgrade() -> None:
    op.drop_table("film_offer_association_table")
    op.drop_table("offers")
