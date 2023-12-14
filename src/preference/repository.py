from _infrastructure.database.base_repository import BaseRepository
from preference.entity import AdopterPreferenceEntity
from preference.model import AdopterPreferenceTyped


class AdopterPreferenceRepository(BaseRepository[AdopterPreferenceTyped, AdopterPreferenceEntity]):
    def __init__(self):
        super().__init__(AdopterPreferenceEntity)

    def delete(self, adopter_id: int, pet_id: int) -> None:
        self.session.query(AdopterPreferenceEntity).filter(
            AdopterPreferenceEntity.adopter_id == adopter_id,
            AdopterPreferenceEntity.pet_id == pet_id
        ).delete()
        self.session.commit()
