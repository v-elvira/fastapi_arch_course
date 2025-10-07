from src.models.hotels import HotelsORM  # import each model

# from src.models import hotels          # the whole file is also OK (without import: nothing detected)
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM  # any one model is OK for alembic to see the file

__all__ = [
    'HotelsORM',
    'RoomsORM',
    'UsersORM',
    'BookingsORM',
    'FacilitiesORM',
]
