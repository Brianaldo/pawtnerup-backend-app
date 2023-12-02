from fastapi import APIRouter

from _common.response import GenericListResponse
from breed.model import Breed, BreedTyped
from breed.service import BreedService


router = APIRouter(
    prefix="/pets/breeds",
    tags=["breeds"]
)


@router.get("", response_model=GenericListResponse[Breed])
async def get_breeds(id: int = None, name: str = None):
    try:
        service = BreedService()
        breeds = service.get_all(id=id, name=name)
        return GenericListResponse(
            message="Retrieved breeds successfully!",
            data=breeds
        )
    except Exception as e:
        print(e)
        raise Exception("Could not retrieve breeds.")
