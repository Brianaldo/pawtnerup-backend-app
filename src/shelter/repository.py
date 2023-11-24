from _infrastructure.database.base_repository import BaseRepository
from shelter.model import Shelter, ShelterDict


class ShelterRepository(BaseRepository[ShelterDict]):
    def __init__(self):
        super().__init__(Shelter)
