from datetime import date
from pet.model import Pet, PetTyped
from pet.repository import PetRepository
import datetime


class PetService:
    def __init__(self):
        self.pet_repo = PetRepository()

    def create_pet(self, estimate_age: float, shelter_email: str, **kwargs: PetTyped) -> Pet:
        estimate_born_date = datetime.datetime.now(
        ) - datetime.timedelta(days=(estimate_age*365.24))
        return self.pet_repo.create(shelter_email=shelter_email, born_date=estimate_born_date, **kwargs).to_model()

    def get_pet_by_shelter(self, shelter_email: str) -> Pet:
        pets = self.pet_repo.fetch_by_shelter(shelter_email=shelter_email)
        return [pet.to_model() for pet in pets]
