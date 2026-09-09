"""add user ownership to film projects

Revision ID: 1f7077603173
Revises: 8745ab60a572
Create Date: 2026-09-10 01:37:21.495357

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1f7077603173"
down_revision: Union[str, Sequence[str], None] = "8745ab60a572"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add the column temporarily as nullable
    op.add_column(
        "film_projects",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # 2. Add the foreign key
    op.create_foreign_key(
        "fk_film_projects_user_id",
        "film_projects",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 3. Assign existing projects to the first registered user
    op.execute(
        """
        UPDATE film_projects
        SET user_id = (
            SELECT id
            FROM users
            ORDER BY id
            LIMIT 1
        )
        WHERE user_id IS NULL
        """
    )

    # 4. Make user_id required
    op.alter_column(
        "film_projects",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # 5. Add index for project ownership lookups
    op.create_index(
        "ix_film_projects_user_id",
        "film_projects",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_film_projects_user_id",
        table_name="film_projects",
    )

    op.drop_constraint(
        "fk_film_projects_user_id",
        "film_projects",
        type_="foreignkey",
    )

    op.drop_column(
        "film_projects",
        "user_id",
    )