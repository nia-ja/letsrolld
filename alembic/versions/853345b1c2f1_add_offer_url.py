"""add-offer-url

Revision ID: 853345b1c2f1
Revises: fef03ede01d5
Create Date: 2024-05-19 13:17:02.274667

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "853345b1c2f1"
down_revision: Union[str, None] = "fef03ede01d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "film_offer_association_table", sa.Column("url", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("film_offer_association_table", "url")
