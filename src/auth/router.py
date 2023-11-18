from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

import auth
from auth import service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/shelter/login")
async def shelter_login():
    try:
        authorization_url, _ = auth.service.get_shelter_authorization_url()

        return RedirectResponse(url=authorization_url)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not log in."
        )


@router.get("/shelter/callback")
async def shelter_login_callback(request: Request):
    try:
        code = request.query_params.get('code')
        shelter_data, token, refresh_token = auth.service.generate_shelter_token(
            code=code)

        return {
            "message": "Logged in successfully!",
            "data": shelter_data,
            "token": {
                "access_token": token,
                "refresh_token": refresh_token
            },
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not log in."
        )


class RefreshTokenRequestBody(BaseModel):
    refresh_token: str


@router.post("/shelter/refresh-token")
async def shelter_refresh_token(body: RefreshTokenRequestBody):
    try:
        shelter_data, token, refresh_token = auth.service.refresh_shelter_token(
            refresh_token=body.refresh_token
        )

        return {
            "message": "Logged in successfully!",
            "data": shelter_data,
            "token": {
                "access_token": token,
                "refresh_token": refresh_token
            },
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not refresh."
        )
