"""rename prop discription to description

Revision ID: 8ddbfeedef98
Revises: 651212c20ec6
Create Date: 2026-09-08 16:54:30.716241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ddbfeedef98'
down_revision: Union[str, Sequence[str], None] = '651212c20ec6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
