"""add primary keys to association tables

Revision ID: 6aeef95710d1
Revises: 4cb954338884
Create Date: 2024-03-15 21:59:32.775104

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "6aeef95710d1"
down_revision: Union[str, None] = "4cb954338884"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("director_film_association_table") as batch_op:
        batch_op.create_primary_key("primary", ["film_id", "director_id"])
    with op.batch_alter_table("film_genre_association_table") as batch_op:
        batch_op.create_primary_key("primary", ["film_id", "genre_id"])
    with op.batch_alter_table("film_country_association_table") as batch_op:
        batch_op.create_primary_key("primary", ["film_id", "country_id"])
    with op.batch_alter_table("film_offer_association_table") as batch_op:
        batch_op.create_primary_key("primary", ["film_id", "offer_id"])


def downgrade() -> None:
    # too lazy to write the downgrades
    pass
