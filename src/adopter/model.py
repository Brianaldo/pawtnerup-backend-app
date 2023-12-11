from typing import TypedDict, Union

from pydantic import BaseModel

from preference.model import AdopterPreference


class AdopterTyped(TypedDict, total=False):
    id: str
    name: str
    email: str
    profile_picture: str


class Adopter(BaseModel):
    id: str
    name: str
    email: str
    profile_picture: str
    preferences: Union[list[AdopterPreference], None]
