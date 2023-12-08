from preference.model import AdopterPreference, AdopterPreferenceTyped
from preference.repository import AdopterPreferenceRepository


class AdopterPreferenceService:
    def __init__(self):
        self.preference_repository = AdopterPreferenceRepository()

    def create_preference(self, **kwargs: AdopterPreferenceTyped) -> AdopterPreference:
        return self.preference_repository.create(**kwargs).to_model()
