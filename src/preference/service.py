from preference.model import AdopterPreference, AdopterPreferenceTyped
from preference.repository import AdopterPreferenceRepository


class AdopterPreferenceService:
    def __init__(self):
        self.preference_repository = AdopterPreferenceRepository()

    def create_preference(self, **kwargs: AdopterPreferenceTyped) -> AdopterPreference:
        return self.preference_repository.create(**kwargs).to_model()

    def delete_preference(self, adopter_id: int, pet_id: int) -> None:
        return self.preference_repository.delete(
            adopter_id=adopter_id, pet_id=pet_id
        )
