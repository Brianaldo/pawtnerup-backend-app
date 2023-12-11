from fastapi import APIRouter, Query

from _common.response import GenericListResponse
from breed.model import Breed, BreedSizeEnum, BreedTyped
from breed.service import BreedService


router = APIRouter(
    prefix="/pets/breeds",
    tags=["breeds"]
)


@router.get("", response_model=GenericListResponse[Breed])
async def get_breeds(id: int = None, name: str = None, size: list[BreedSizeEnum] = Query(None)):
    try:
        service = BreedService()
        breeds = service.get_all(id=id, name=name, size=size)
        return GenericListResponse(
            message="Retrieved breeds successfully!",
            data=breeds
        )
    except Exception as e:
        print(e)
        raise Exception("Could not retrieve breeds.")
