from typing import TypedDict

from pydantic import BaseModel, constr


class AdopterTyped(TypedDict, total=False):
    id: str
    name: str
    email: str
    bio: str
    profile_picture: str


class Adopter(BaseModel):
    id: str
    name: str
    email: str
    bio: str
    profile_picture: str


class CreateAdopterRequestBody(BaseModel):
    bio: constr(strip_whitespace=True, min_length=0, max_length=100)
