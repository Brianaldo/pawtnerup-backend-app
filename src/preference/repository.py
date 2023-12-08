from _infrastructure.database.base_repository import BaseRepository
from preference.entity import AdopterPreferenceEntity
from preference.model import AdopterPreferenceTyped


class AdopterPreferenceRepository(BaseRepository[AdopterPreferenceTyped, AdopterPreferenceEntity]):
    def __init__(self):
        super().__init__(AdopterPreferenceEntity)
