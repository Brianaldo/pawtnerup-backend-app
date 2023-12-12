from fastapi import APIRouter, Depends, HTTPException
from _common.exceptions import NotFoundException
from _common.response import GenericListResponse, GenericObjectResponse
from auth.dependencies import authenticate_shelter

from auth.models import ShelterGoogleUser
from pet.model import CreatePetRequestBody, CreatePetResponseBody, DeletedResponse, Pet, PetMediaRequestBody, PetResponse, PetTrimmedResponse, UpdatePetMediaRequestBody, UpdatePetRequestBody
from pet.service import PetService


router = APIRouter(
    prefix="/shelters/pets",
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
                pet=pet.to_response(),
                post_media_urls=urls
            )
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not create pet."
        )


@router.get("/me", response_model=GenericListResponse[PetTrimmedResponse])
async def get_pets(
    user_context: ShelterGoogleUser = Depends(authenticate_shelter)
):
    try:
        service = PetService()
        pets = service.get_pet_by_shelter(
            shelter_email=user_context.email
        )
        pets = [pet.to_trimmed_response() for pet in pets]

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


@router.get("/{pet_id}", response_model=GenericObjectResponse[PetResponse])
async def get_pet(
    pet_id: str,
    user_context: ShelterGoogleUser = Depends(authenticate_shelter)
):
    try:
        service = PetService()
        pet = service.get_pet(
            shelter_email=user_context.email,
            pet_id=pet_id
        )

        return GenericObjectResponse(
            message="Retrieved pet successfully!",
            data=pet.to_response()
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
            detail="Could not retrieve pet."
        )


@router.put("/{pet_id}", response_model=GenericObjectResponse[PetResponse])
async def update_pet(
    pet_id: str,
    body: UpdatePetRequestBody,
    user_context: ShelterGoogleUser = Depends(authenticate_shelter)
):
    try:
        service = PetService()
        pet = service.update_pet(
            shelter_email=user_context.email,
            pet_id=pet_id,
            **body.model_dump()
        )

        return GenericObjectResponse(
            message="Updated pet successfully!",
            data=pet.to_response()
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
            detail="Could not update pet."
        )


@router.put("/{pet_id}/media", response_model=GenericObjectResponse[CreatePetResponseBody])
async def update_pet_media(
    pet_id: str,
    body: UpdatePetMediaRequestBody,
    user_context: ShelterGoogleUser = Depends(authenticate_shelter)
):
    try:
        service = PetService()
        (pet, urls) = service.update_media(
            shelter_email=user_context.email,
            pet_id=pet_id,
            media=body.media
        )

        return GenericObjectResponse(
            message="Updated pet media successfully!",
            data=CreatePetResponseBody(
                pet=pet.to_response(),
                post_media_urls=urls
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
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
            detail="Could not update pet media."
        )


@router.delete("/{pet_id}", response_model=GenericObjectResponse[DeletedResponse])
async def delete_pet(
    pet_id: str,
    user_context: ShelterGoogleUser = Depends(authenticate_shelter)
):
    try:
        service = PetService()
        deleted_id = service.delete_pet(
            shelter_email=user_context.email,
            pet_id=pet_id
        )

        return GenericObjectResponse(
            message="Deleted pet successfully!",
            data=DeletedResponse(
                id=deleted_id
            )
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
            detail="Could not delete pet."
        )
