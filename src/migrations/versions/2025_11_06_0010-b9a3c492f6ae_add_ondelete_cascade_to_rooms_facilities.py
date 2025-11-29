"""add ondelete=CASCADE to rooms_facilities

Revision ID: b9a3c492f6ae
Revises: c62ecea45e1b
Create Date: 2025-11-06 00:10:13.526355

"""

from typing import Sequence, Union

from alembic import op
# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9a3c492f6ae'
down_revision: Union[str, None] = 'c62ecea45e1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('rooms_facilities_room_id_fkey', 'rooms_facilities', type_='foreignkey')
    op.drop_constraint('rooms_facilities_facility_id_fkey', 'rooms_facilities', type_='foreignkey')
    op.create_foreign_key(
        'my_rooms_facilities_facility_id_fkey',
        'rooms_facilities',
        'facilities',
        ['facility_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'my_rooms_facilities_room_id_fkey', 'rooms_facilities', 'rooms', ['room_id'], ['id'], ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('my_rooms_facilities_facility_id_fkey', 'rooms_facilities', type_='foreignkey')
    op.drop_constraint('my_rooms_facilities_room_id_fkey', 'rooms_facilities', type_='foreignkey')
    op.create_foreign_key(
        'rooms_facilities_facility_id_fkey',
        'rooms_facilities',
        'facilities',
        ['facility_id'],
        ['id'],
    )
    op.create_foreign_key(
        'rooms_facilities_room_id_fkey',
        'rooms_facilities',
        'rooms',
        ['room_id'],
        ['id'],
    )
