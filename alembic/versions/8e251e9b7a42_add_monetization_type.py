"""add-monetization-type

Revision ID: 8e251e9b7a42
Revises: 853345b1c2f1
Create Date: 2024-11-30 12:50:24.880021

"""

from typing import Sequence, Union

# TODO: Fix type ignore by moving alembic/ directory?
from alembic import op  # type: ignore[attr-defined]
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8e251e9b7a42"
down_revision: Union[str, None] = "853345b1c2f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "offers",
        sa.Column(
            "monetization_type",
            sa.Enum(
                "FREE",
                "FLATRATE",
                "RENT",
                "BUY",
                "CINEMA",
                "ADS",
                "FAST",
                "DISC",
                name="monetizationtype",
            ),
        ),
    )


def downgrade() -> None:
    op.drop_column("offers", "monetization_type")
