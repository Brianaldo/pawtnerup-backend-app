import enum
from typing import TypedDict, Union
from pydantic import BaseModel


class BreedSizeEnum(enum.Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    BIG = "BIG"
    GIANT = "GIANT"


class BreedTyped(TypedDict, total=False):
    id: int
    name: str
    size: BreedSizeEnum


class Breed(BaseModel):
    id: int
    name: str
    size: Union[BreedSizeEnum, None]
