"""Add users

Revision ID: e61cf1963534
Revises: cde5b29ad466
Create Date: 2025-07-18 23:38:57.829154

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e61cf1963534'
down_revision: Union[str, None] = 'cde5b29ad466'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False),
        sa.Column('hashed_password', sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
