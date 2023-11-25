from typing import Annotated, Union
from fastapi import Depends, HTTPException, Request
from auth.exceptions import UnauthorizedError
from auth.models import AdopterGoogleUser, ShelterGoogleUser

from auth.service import AuthService


def auth_middleware(request: Request) -> Union[ShelterGoogleUser, AdopterGoogleUser]:
    try:
        access_token = request.headers.get('Authorization')
        access_token = access_token.split(' ')[1]

        service = AuthService()

        return service.get_user_from_token(token=access_token)
    except AttributeError or IndexError:
        raise HTTPException(
            status_code=401,
            detail="Could not find token."
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not authenticate."
        )


def authenticate_shelter(info: Union[ShelterGoogleUser, AdopterGoogleUser] = Depends(auth_middleware)) -> ShelterGoogleUser:
    if info.role != 'SHELTER':
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )
    return info


def authenticate_adopter(info: Union[ShelterGoogleUser, AdopterGoogleUser] = Depends(auth_middleware)) -> AdopterGoogleUser:
    if info.role != 'ADOPTER':
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )
    return info
