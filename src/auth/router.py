from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.responses import RedirectResponse

import auth
from auth.constant import AUTH_ACCESS_TOKEN_COOKIE, AUTH_REFRESH_TOKEN_COOKIE
from auth.dependencies import verify_token

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
async def shelter_login_callback(request: Request, response: Response):
    try:
        code = request.query_params.get('code')
        shelter_data, token, refresh_token = auth.service.generate_shelter_token(
            code=code)

        response.set_cookie(key=AUTH_ACCESS_TOKEN_COOKIE,
                            value='Bearer ' + token,
                            httponly=True,
                            path="/"
                            )
        response.set_cookie(key=AUTH_REFRESH_TOKEN_COOKIE,
                            value=refresh_token,
                            httponly=True,
                            path="/"
                            )

        return {
            "message": "Logged in successfully!",
            "data": shelter_data
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not log in."
        )


@router.get("/logout")
async def logout(_: Annotated[dict, Depends(verify_token)], response: Response):
    try:
        response.delete_cookie(key=AUTH_ACCESS_TOKEN_COOKIE, path="/")
        response.delete_cookie(key=AUTH_REFRESH_TOKEN_COOKIE, path="/")

        return {
            "message": "Logged out successfully!"
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not log out."
        )
