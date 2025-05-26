"""Create collation ci text

Revision ID: d05f884dedf8
Revises:
Create Date: 2025-05-24 19:27:33.419081

"""

from typing import Sequence, Union

from alembic import op

from core.constants import COLLATION_CI_TEXT_NAME

# revision identifiers, used by Alembic.
revision: str = "d05f884dedf8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        f"""
        CREATE COLLATION IF NOT EXISTS {COLLATION_CI_TEXT_NAME}(
            provider = icu,
            locale = 'und-u-ks-level2',
            deterministic = false
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        f"""
        DROP COLLATION IF EXISTS {COLLATION_CI_TEXT_NAME};
        """
    )
