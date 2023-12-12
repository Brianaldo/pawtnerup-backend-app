from datetime import date
from pydantic import BaseModel
from pet.model import AgeEnum, GenderEnum, Pet
from pet.repository import PetRepository
import pandas as pd


class InputData(BaseModel):
    gender: list[GenderEnum]
    age: list[AgeEnum]
    breed: list[str]


class PetData(BaseModel):
    id: list[int]
    name: list[str]
    gender: list[str]
    breed: list[str]
    age: list[str]


class ContentBasedFilteringModel:
    def __init__(self):
        pet_repo = PetRepository()
        pets = pet_repo.get_by_filter()
        pet_data = PetData(
            id=[],
            name=[],
            gender=[],
            breed=[],
            age=[]
        )

        for pet in pets:
            pet = pet.to_model()
            pet_data.id.append(pet.id)
            pet_data.name.append(pet.name)
            pet_data.gender.append(pet.gender.to_str())
            pet_data.breed.append(pet.breed)
            estimate_age = round(
                (date.today() - pet.born_date).days / 365.24, 1)
            age = AgeEnum.from_float(estimate_age)
            pet_data.age.append(age.to_str())

        self.pets = list(map(lambda pet: pet.to_model(), pets))
        self.pet_df = pd.DataFrame.from_dict(pet_data.model_dump())

    def calc_custom_similarity(self, pet: Pet, adopter: InputData, weights: tuple[int, int, int]):
        similarity = 0

        breed_weight, gender_weight, age_weight = weights

        if pet.breed in adopter.breed:
            similarity += breed_weight

        if AgeEnum.from_float(pet.to_trimmed_response().estimate_age) in adopter.age:
            similarity += age_weight

        if pet.gender in adopter.gender:
            similarity += gender_weight

        return similarity

    def get_most_similar(self, data: InputData) -> list[Pet]:
        result = []
        for pet in self.pets:
            similarity = self.calc_custom_similarity(
                pet, data, (2, 1, 1)
            )
            result.append((pet, similarity))

        result.sort(key=lambda el: el[1], reverse=True)
        return list(map(lambda el: el[0], result))
