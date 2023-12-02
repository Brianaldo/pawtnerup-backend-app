from typing import TypedDict
from pydantic import BaseModel, EmailStr, constr
from pydantic_extra_types.phone_numbers import PhoneNumber


class ShelterTyped(TypedDict, total=False):
    id: int
    name: str
    email: str
    contact_email: str
    address: str
    phone_number: str


class Shelter(BaseModel):
    id: int
    name: str
    email: str
    contact_email: str
    address: str
    phone_number: PhoneNumber


class CreateShelterRequestBody(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=50)
    phone_number: PhoneNumber
    contact_email: EmailStr
    address: constr(strip_whitespace=True, min_length=1, max_length=50)
