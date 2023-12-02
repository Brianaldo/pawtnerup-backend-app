from typing import Union
from _infrastructure.database.exceptions import AlreadyExistsError, NotFoundError
from shelter.exceptions import ShelterAlreadyExists, ShelterNotFound
from shelter.model import Shelter, ShelterTyped
from shelter.repository import ShelterRepository


class ShelterService:
    def __init__(self):
        self.shelter_repo = ShelterRepository()

    def get_shelter(self, **kwargs: ShelterTyped) -> None:
        try:
            shelter = self.shelter_repo.get_one_by_filter(**kwargs)
            return shelter.to_model()
        except NotFoundError:
            raise ShelterNotFound('Shelter not found.')
        except Exception as e:
            print("ShelterService::get_shelter: ", e)
            raise e

    def get_shelters(self, **kwargs: ShelterTyped) -> list[Shelter]:
        shelters = self.shelter_repo.get_by_filter(**kwargs)
        return [shelter.to_model() for shelter in shelters]

    def create_shelter(self, **kwargs: ShelterTyped) -> Shelter:
        try:
            return self.shelter_repo.create(**kwargs).to_model()
        except AlreadyExistsError:
            raise ShelterAlreadyExists('Shelter already exists.')
        except Exception as e:
            print("ShelterService::create_shelter: ", e)
            raise e

    def update_shelter(self, shelter_id: int, **kwargs: ShelterTyped) -> Shelter:
        try:
            shelter = self.shelter_repo.update(shelter_id, **kwargs)
            return shelter.to_model()
        except NotFoundError:
            raise ShelterNotFound('Shelter not found.')
        except Exception as e:
            print("ShelterService::update_shelter: ", e)
            raise e

    def delete_shelter(self, shelter_id: int) -> None:
        try:
            self.shelter_repo.delete(shelter_id)
        except NotFoundError:
            raise ShelterNotFound('Shelter not found.')
        except Exception as e:
            print("ShelterService::delete_shelter: ", e)
            raise e
