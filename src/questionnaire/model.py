from typing import TypedDict

from pydantic import BaseModel, constr
from adopter.model import Adopter

from breed.model import BreedSizeEnum
from pet.model import AgeEnum, GenderEnum


class QuestionnaireTyped(TypedDict, total=False):
    id: int
    adopter_id: str
    pet_sizes: list[BreedSizeEnum]
    pet_ages: list[AgeEnum]
    pet_genders: list[GenderEnum]
    breeds: list[str]
    breed_ids: list[int]


class Questionnaire(BaseModel):
    id: int
    adopter_id: str
    adopter: Adopter
    pet_sizes: list[BreedSizeEnum]
    pet_ages: list[AgeEnum]
    pet_genders: list[GenderEnum]
    breeds: list[str]


class CreateQuestionnaire(BaseModel):
    pet_sizes: list[BreedSizeEnum]
    pet_ages: list[AgeEnum]
    pet_genders: list[GenderEnum]
    breed_ids: list[int]
