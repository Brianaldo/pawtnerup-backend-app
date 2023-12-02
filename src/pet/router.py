from fastapi import APIRouter, Depends, HTTPException
from _common.exceptions import NotFoundException
from _common.response import GenericListResponse, GenericObjectResponse
from auth.dependencies import authenticate_shelter

from auth.models import ShelterGoogleUser
from pet.model import CreatePetRequestBody, CreatePetResponseBody, Pet
from pet.service import PetService


router = APIRouter(
    prefix="/shelters/me/pets",
    tags=["pets"]
)


@router.post("", response_model=GenericObjectResponse[CreatePetResponseBody])
async def create_pet(
    body: CreatePetRequestBody,
    user_context: ShelterGoogleUser = Depends(authenticate_shelter)
):
    try:
        service = PetService()
        (pet, urls) = service.create_pet(
            shelter_email=user_context.email,
            **body.model_dump()
        )

        return GenericObjectResponse(
            message="Created pet successfully!",
            data=CreatePetResponseBody(
                pet=pet,
                post_media_urls=urls
            )
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not create pet."
        )


@router.get("", response_model=GenericListResponse[Pet])
async def get_pets(
    user_context: ShelterGoogleUser = Depends(authenticate_shelter)
):
    try:
        service = PetService()
        pets = service.get_pet_by_shelter(
            shelter_email=user_context.email
        )

        return GenericListResponse(
            message="Retrieved pets successfully!",
            data=pets
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve pets."
        )
