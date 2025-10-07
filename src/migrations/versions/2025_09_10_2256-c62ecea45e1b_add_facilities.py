"""Add facilities

Revision ID: c62ecea45e1b
Revises: 169ba2e8ee4b
Create Date: 2025-09-10 22:56:42.445104

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c62ecea45e1b'
down_revision: Union[str, None] = '169ba2e8ee4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'facilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'rooms_facilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('facility_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['facility_id'],
            ['facilities.id'],
        ),
        sa.ForeignKeyConstraint(
            ['room_id'],
            ['rooms.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('rooms_facilities')
    op.drop_table('facilities')
