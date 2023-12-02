from typing import TypedDict
from pydantic import BaseModel


class BreedTyped(TypedDict, total=False):
    id: int
    name: str


class Breed(BaseModel):
    id: int
    name: str
