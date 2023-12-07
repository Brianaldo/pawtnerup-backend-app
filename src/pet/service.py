from datetime import date
from _infrastructure.object_storage.client import ObjectStorageClient
from pet.model import Pet, PetTyped
from pet.repository import PetRepository
import datetime

from shelter.repository import ShelterRepository


class PetService:
    def __init__(self):
        self.pet_repo = PetRepository()
        self.shelter_repo = ShelterRepository()
        self.storage_client = ObjectStorageClient()

    def create_pet(self, estimate_age: float, shelter_email: str, **kwargs: PetTyped) -> tuple[Pet, list[str]]:
        estimate_born_date = datetime.datetime.now(
        ) - datetime.timedelta(days=(estimate_age*365.24))

        post_media_urls: list[str] = []
        for i in range(len(kwargs.get('media'))):
            ext = kwargs.get('media')[i].split('.')[-1]
            new_filename, url = self.storage_client.post_presigned_url(
                ext
            )
            post_media_urls.append(url)
            kwargs.get('media')[i] = new_filename

        return (self.pet_repo.create(shelter_email=shelter_email, born_date=estimate_born_date, **kwargs).to_model(), post_media_urls)

    def get_pet_by_shelter(self, shelter_email: str) -> list[Pet]:
        pets = self.pet_repo.fetch_by_shelter(shelter_email=shelter_email)
        return [pet.to_model() for pet in pets]

    def get_pet(self, shelter_email: str, pet_id: int) -> Pet:
        shelter = self.shelter_repo.get_one_by_filter(
            email=shelter_email
        )
        pet = self.pet_repo.get_one_by_filter(
            shelter_id=shelter.id,
            id=pet_id
        )

        return pet.to_model()
