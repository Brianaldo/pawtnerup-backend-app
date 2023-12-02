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
    authuser: str
    code: str
    hd: str
    prompt: str
    scope: str


class RefreshTokenRequestBody(BaseModel):
    refresh_token: str


class LoginResponse(ShelterGoogleUser, BaseModel):
    access_token: str
    refresh_token: Union[str, None]
