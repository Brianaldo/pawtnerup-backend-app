from typing import Union
from pydantic import BaseModel


class GoogleUser(BaseModel):
    id: str
    email: str
    name: str
    picture: str
    given_name: str
    family_name: str


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
