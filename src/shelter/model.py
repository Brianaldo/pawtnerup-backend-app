from typing import TypedDict
from pydantic import BaseModel


class ShelterTyped(TypedDict, total=False):
    id: int
    name: str
    email: str
    address: str
    phone_number: str


class Shelter(BaseModel):
    id: int
    name: str
    email: str
    address: str
    phone_number: str


class CreateShelterRequestBody(BaseModel):
    name: str
    phone_number: str
    address: str
