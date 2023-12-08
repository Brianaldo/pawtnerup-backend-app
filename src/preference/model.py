import enum
from typing import TypedDict, Union

from pydantic import BaseModel

from pet.model import Pet


class PreferenceEnum(enum.Enum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"


class AdopterPreferenceTyped(TypedDict, total=False):
    adopter_id: str
    pet_id: int
    preference: PreferenceEnum


class AdopterPreference(BaseModel):
    pet_id: int
    pet: Union[Pet, None]
    preference: PreferenceEnum


class CreateAdopterPreferenceRequestBody(BaseModel):
    pet_id: int
    preference: PreferenceEnum
