"""Create pgcrypto extention

Revision ID: 2ba78492f417
Revises: d05f884dedf8
Create Date: 2025-05-24 20:36:49.096258

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2ba78492f417"
down_revision: Union[str, None] = "d05f884dedf8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DROP EXTENSION IF EXISTS "pgcrypto";')
