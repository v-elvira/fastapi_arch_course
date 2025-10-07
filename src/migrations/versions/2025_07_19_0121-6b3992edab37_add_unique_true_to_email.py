"""add unique=True to email

Revision ID: 6b3992edab37
Revises: e61cf1963534
Create Date: 2025-07-19 01:21:50.799991

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '6b3992edab37'
down_revision: Union[str, None] = 'e61cf1963534'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('unique_email', 'users', ['email'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('unique_email', 'users', type_='unique')
