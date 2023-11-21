from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

M = TypeVar("M", bound=BaseModel)


class BaseGenericResponse(GenericModel):
    message: str


class GenericObjectResponse(BaseGenericResponse, Generic[M]):
    data: M


class GenericListResponse(BaseGenericResponse, Generic[M]):
    data: list[M]
