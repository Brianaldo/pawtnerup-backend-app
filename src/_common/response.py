from typing import Generic, TypeVar
from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


class BaseGenericResponse(BaseModel):
    message: str


class GenericObjectResponse(BaseGenericResponse, Generic[M]):
    data: M


class GenericListResponse(BaseGenericResponse, Generic[M]):
    data: list[M]
