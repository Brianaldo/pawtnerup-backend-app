from _infrastructure.database.base_repository import BaseRepository
from shelter.model import ShelterTyped
from shelter.entity import ShelterEntity


class ShelterRepository(BaseRepository[ShelterTyped, ShelterEntity]):
    def __init__(self):
        super().__init__(ShelterEntity)
