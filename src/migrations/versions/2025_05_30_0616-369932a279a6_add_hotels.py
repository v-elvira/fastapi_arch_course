"""add hotels

Revision ID: 369932a279a6
Revises:
Create Date: 2025-05-30 06:16:08.378797

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '369932a279a6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'hotels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('hotels')
