"""rename prop discription to description

Revision ID: 0981dcf43c18
Revises: 8ddbfeedef98
Create Date: 2026-09-08 17:23:12.028687

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0981dcf43c18"
down_revision: Union[str, Sequence[str], None] = "8ddbfeedef98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename props.discription to props.description."""
    op.alter_column(
        "props",
        "discription",
        new_column_name="description",
    )


def downgrade() -> None:
    """Rename props.description back to props.discription."""
    op.alter_column(
        "props",
        "description",
        new_column_name="discription",
    )