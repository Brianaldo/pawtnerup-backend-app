from fastapi import APIRouter, Depends, HTTPException
from _common import *
from auth.dependencies import authenticate_shelter
from auth.models import ShelterGoogleUser
from shelter.exceptions import ShelterAlreadyExists, ShelterNotFound
from shelter.model import CreateShelterRequestBody, Shelter
from shelter.service import ShelterService

router = APIRouter(
    prefix="/shelters",
    tags=["shelters"]
)


@router.get("/me", response_model=GenericObjectResponse[Shelter])
async def get_shelter(user_context: ShelterGoogleUser = Depends(authenticate_shelter)):
    try:
        service = ShelterService()
        shelter = service.get_shelter(email=user_context.email)
        return GenericObjectResponse(
            message="Retrieved shelters successfully!",
            data=shelter
        )
    except ShelterNotFound:
        raise HTTPException(
            status_code=403,
            detail="Unregistered shelter."
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve shelters."
        )


@router.post("", response_model=GenericObjectResponse[Shelter])
async def create_shelter(
    body: CreateShelterRequestBody,
    user_context: ShelterGoogleUser = Depends(authenticate_shelter)
):
    try:
        service = ShelterService()
        shelter = service.create_shelter(
            name=body.name,
            address=body.address,
            phone_number=body.phone_number,
            contact_email=body.contact_email,
            email=user_context.email
        )
        return GenericObjectResponse(
            message="Created shelter successfully!",
            data=shelter
        )
    except ShelterAlreadyExists:
        raise HTTPException(
            status_code=400,
            detail="Shelter already exists."
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not create shelter."
        )
