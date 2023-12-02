from breed.model import Breed, BreedTyped
from breed.repository import BreedRepository


class BreedService:
    def __init__(self):
        self.breed_repository = BreedRepository()

    def get_all(self, **kwargs: BreedTyped) -> list[Breed]:
        breeds = self.breed_repository.get_by_filter(**kwargs)
        return [breed.to_model() for breed in breeds]

    def create(self, breed: Breed) -> Breed:
        return self.breed_repository.create(breed)
