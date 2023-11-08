from fastapi import HTTPException, Request

from auth.constant import AUTH_ACCESS_TOKEN_COOKIE
from auth.service import get_user_from_token


def verify_token(request: Request) -> dict:
    try:
        access_token = request.cookies.get(AUTH_ACCESS_TOKEN_COOKIE)
        access_token = access_token.split(' ')[1]
    except AttributeError:
        raise HTTPException(
            status_code=401,
            detail="Could not find token."
        )
    except IndexError:
        raise HTTPException(
            status_code=401,
            detail="Could not parse token."
        )

    return get_user_from_token(token=access_token)
