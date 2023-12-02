from datetime import date
import enum
from typing import TypedDict, Union
from pydantic import BaseModel, constr


class GenderEnum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class SterilizationEnum(enum.Enum):
    NEUTERED = "NEUTERED"
    SPAYED = "SPAYED"


class PetTyped(TypedDict, total=False):
    id: int
    name: str
    gender: GenderEnum
    breed: str
    shelter_id: int
    born_date: date
    sterilization_status: SterilizationEnum
    rescue_story: Union[str, None]
    media: list[str]


class Pet(BaseModel):
    id: int
    name: str
    gender: GenderEnum
    breed: str
    born_date: date
    shelter_id: int
    sterilization_status: SterilizationEnum
    rescue_story: Union[str, None]
    media: list[str]


class CreatePetRequestBody(BaseModel):
    name: constr(strip_whitespace=True)
    gender: GenderEnum
    breed: constr(strip_whitespace=True)
    estimate_age: float
    sterilization_status: SterilizationEnum
    rescue_story: Union[constr(strip_whitespace=True), None]
    media: list[str] = []


class CreatePetResponseBody(BaseModel):
    pet: Pet
    post_media_urls: list[str]
