from typing import Annotated, Union
from fastapi import Depends, HTTPException, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth.exceptions import UnauthorizedError
from auth.models import AdopterGoogleUser, ShelterGoogleUser

from auth.service import AuthService

security_scheme = HTTPBearer()


def auth_middleware(token: HTTPAuthorizationCredentials = Depends(security_scheme)) -> Union[ShelterGoogleUser, AdopterGoogleUser]:
    try:
        service = AuthService()

        return service.get_user_from_token(token=token.credentials)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def authenticate_shelter(info: Union[ShelterGoogleUser, AdopterGoogleUser] = Depends(auth_middleware)) -> ShelterGoogleUser:
    if info.role != 'SHELTER':
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )
    return info


def authenticate_adopter(
        x_refresh_token: Annotated[Union[str, None], Header()] = None,
        token: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> AdopterGoogleUser:
    try:
        service = AuthService(isShelter=False)
        info = service.get_user_from_token(
            token=token.credentials
        )

        if info.role != 'ADOPTER':
            raise HTTPException(
                status_code=403,
                detail="Forbidden."
            )

        return info
    except Exception:
        if x_refresh_token is None:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized."
            )
        try:
            (info, _, _) = service.refresh_token(
                refresh_token=x_refresh_token,
            )

            return info
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=401,
                detail="Unauthorized."
            )
