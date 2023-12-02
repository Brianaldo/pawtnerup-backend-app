from _infrastructure.database.base_repository import BaseRepository
from adopter.entity import AdopterEntity
from adopter.model import AdopterTyped


class AdopterRepository(BaseRepository[AdopterTyped, AdopterEntity]):
    def __init__(self):
        super().__init__(AdopterEntity)
