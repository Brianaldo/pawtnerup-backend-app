from fastapi import APIRouter, HTTPException
from _common import *

from auth.models import GenerateRefreshTokenRequestBody, LoginCallbackRequestBody, LoginResponse, RefreshTokenRequestBody, ShelterGoogleUser
import auth.service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/shelter/oauth2callback", response_model=GenericObjectResponse[LoginResponse])
async def shelter_oauth2_callback(body: LoginCallbackRequestBody):
    try:
        service = auth.service.AuthService()
        shelter_data, token, refresh_token = service.generate_token(
            code=body.code
        )

        return GenericObjectResponse(
            message="Logged in successfully!",
            data=LoginResponse(**shelter_data.model_dump(),
                               access_token=token,
                               refresh_token=refresh_token
                               )
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not log in."
        )


@router.post("/shelter/refresh-token", response_model=GenericObjectResponse[LoginResponse])
async def shelter_refresh_token(body: RefreshTokenRequestBody):
    try:
        service = auth.service.AuthService()
        shelter_data, token, refresh_token = service.refresh_token(
            refresh_token=body.refresh_token
        )

        return GenericObjectResponse(
            message="Refreshed successfully!",
            data=LoginResponse(**shelter_data.model_dump(),
                               access_token=token,
                               refresh_token=refresh_token
                               )
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not refresh."
        )


@router.post("/adopter/generate-refresh-token", response_model=GenericObjectResponse[LoginResponse])
async def adopter_generate_refresh_token(body: GenerateRefreshTokenRequestBody):
    try:
        service = auth.service.AuthService(isShelter=False)
        adopter_data, token, refresh_token = service.generate_token(
            code=body.code
        )

        return GenericObjectResponse(
            message="Logged in successfully!",
            data=LoginResponse(**adopter_data.model_dump(),
                               access_token=token,
                               refresh_token=refresh_token
                               )
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not log in."
        )
