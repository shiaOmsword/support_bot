"""baseline

Revision ID: 277097b104f4
Revises: b0d63a1dd8cf
Create Date: 2026-01-28 04:31:03.985434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '277097b104f4'
down_revision: Union[str, Sequence[str], None] = 'b0d63a1dd8cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
