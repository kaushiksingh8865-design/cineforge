"""create users table

Revision ID: 8745ab60a572
Revises: 0981dcf43c18
Create Date: 2026-09-10 00:22:07.884785

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8745ab60a572"
down_revision: Union[str, Sequence[str], None] = "0981dcf43c18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_users_username",
        "users",
        ["username"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_users_username",
        table_name="users",
    )

    op.drop_table("users")