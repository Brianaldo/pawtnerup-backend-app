from datetime import date
import enum
from typing import TypedDict, Union
from pydantic import BaseModel, constr

from _infrastructure.object_storage.configs import CLOUD_STORAGE_BUCKET


class GenderEnum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class SterilizationEnum(enum.Enum):
    NEUTERED = "NEUTERED"
    SPAYED = "SPAYED"
    NOT_STERILIZED = "NOT_STERILIZED"
    VACCINATED = "VACCINATED"


class AgeEnum(enum.Enum):
    # 0 - 6 months
    PUPPY = "PUPPY"
    # 6 - 12 months
    YOUNG = "YOUNG"
    # 1 - 7 years
    ADULT = "ADULT"
    # > 7 years
    SENIOR = "SENIOR"


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


class PetTrimmedResponse(BaseModel):
    id: int
    name: str
    gender: GenderEnum
    breed: str
    estimate_age: float
    sterilization_status: SterilizationEnum


class PetResponse(BaseModel):
    id: int
    name: str
    gender: GenderEnum
    breed: str
    estimate_age: float
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

    def to_response(self) -> PetResponse:
        estimate_age = round((date.today() - self.born_date).days / 365.24, 1)
        return PetResponse(
            id=self.id,
            name=self.name,
            gender=self.gender,
            breed=self.breed,
            estimate_age=estimate_age,
            sterilization_status=self.sterilization_status,
            rescue_story=self.rescue_story,
            media=map(
                lambda url: "https://storage.googleapis.com/{}/{}".format(CLOUD_STORAGE_BUCKET, url), self.media),
        )

    def to_trimmed_response(self) -> PetTrimmedResponse:
        estimate_age = round((date.today() - self.born_date).days / 365.24, 1)
        return PetTrimmedResponse(
            id=self.id,
            name=self.name,
            gender=self.gender,
            breed=self.breed,
            estimate_age=estimate_age,
            sterilization_status=self.sterilization_status,
        )


class CreatePetRequestBody(BaseModel):
    name: constr(strip_whitespace=True)
    gender: GenderEnum
    breed: constr(strip_whitespace=True)
    estimate_age: float
    sterilization_status: SterilizationEnum
    rescue_story: Union[constr(strip_whitespace=True), None]
    media: list[str] = []


class CreatePetResponseBody(BaseModel):
    pet: PetResponse
    post_media_urls: list[Union[str, None]]


class PetMediaTypeRequest(enum.Enum):
    DELETE = "DELETE"
    ADD = "ADD"
    UPDATE = "UPDATE"
    DO_NOTHING = "DO_NOTHING"


class PetMediaRequestBody(BaseModel):
    type: PetMediaTypeRequest
    filename: str


class UpdatePetMediaRequestBody(BaseModel):
    media: list[PetMediaRequestBody] = []


class DeletedResponse(BaseModel):
    id: int
