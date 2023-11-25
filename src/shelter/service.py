from shelter.model import Shelter, ShelterTyped
from shelter.repository import ShelterRepository


class ShelterService:
    def __init__(self):
        self.shelter_repo = ShelterRepository()

    def get_shelter(self, **kwargs: ShelterTyped) -> Shelter:
        return self.shelter_repo.get_one_by_filter(**kwargs).to_model()

    def get_shelters(self, **kwargs: ShelterTyped) -> list[Shelter]:
        return self.shelter_repo.get_by_filter(**kwargs).map(lambda shelter: shelter.to_model())

    def create_shelter(self, **kwargs: ShelterTyped) -> Shelter:
        return self.shelter_repo.create(**kwargs).to_model()

    def update_shelter(self, shelter_id: int, **kwargs: ShelterTyped) -> Shelter:
        return self.shelter_repo.update(shelter_id, **kwargs).to_model()

    def delete_shelter(self, shelter_id: int) -> None:
        return self.shelter_repo.delete(shelter_id)
