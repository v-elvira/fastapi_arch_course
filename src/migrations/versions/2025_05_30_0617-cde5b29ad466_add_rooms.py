"""add rooms

Revision ID: cde5b29ad466
Revises: 369932a279a6
Create Date: 2025-05-30 06:17:29.942005

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cde5b29ad466'
down_revision: Union[str, None] = '369932a279a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hotel_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['hotel_id'],
            ['hotels.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('rooms')
