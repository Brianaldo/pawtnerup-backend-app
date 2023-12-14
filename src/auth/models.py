from typing import Optional, Union
from pydantic import BaseModel


class GoogleUser(BaseModel):
    id: str
    email: str
    name: Union[str, None]
    picture: Union[str, None]
    given_name: Union[str, None]
    family_name: Union[str, None]


class ShelterGoogleUser(GoogleUser):
    role: str = "SHELTER"


class AdopterGoogleUser(GoogleUser):
    role: str = "ADOPTER"


class LoginCallbackRequestBody(BaseModel):
    authuser: Union[str, None]
    code: str
    hd: Union[str, None]
    prompt: Union[str, None]
    scope: Union[str, None]


class RefreshTokenRequestBody(BaseModel):
    refresh_token: str


class LoginResponse(ShelterGoogleUser, BaseModel):
    access_token: str
    refresh_token: Union[str, None]


class GenerateRefreshTokenRequestBody(BaseModel):
    code: str
