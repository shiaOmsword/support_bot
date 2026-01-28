"""add blocked_until

Revision ID: b0d63a1dd8cf
Revises: 4df4c155ea2a
Create Date: 2026-01-28 04:21:41.703807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0d63a1dd8cf'
down_revision: Union[str, Sequence[str], None] = '4df4c155ea2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
