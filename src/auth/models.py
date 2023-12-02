from typing import Optional, Union
from pydantic import BaseModel


class GoogleUser(BaseModel):
    id: str
    email: str
    name: Optional[str]
    picture: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]


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
