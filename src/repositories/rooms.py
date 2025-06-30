from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM

class HotelsRepository(BaseRepository):
    model = RoomsORM
