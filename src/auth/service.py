from typing import Union
from cachecontrol import CacheControl
import requests
import google_auth_oauthlib.flow
from google.oauth2 import id_token
import google.oauth2.credentials
import google.auth.transport.requests

from auth.configs import GOOGLE_ADOPTER_CLIENT_ID, GOOGLE_SHELTER_CLIENT_ID, GOOGLE_SHELTER_CLIENT_SECRET, SHELTER_CLIENT_SECRET_FILE
from auth.exceptions import UnauthorizedError
from auth.models import AdopterGoogleUser, GoogleUser, ShelterGoogleUser


class AuthService:
    def __init__(self) -> None:
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secrets_file=SHELTER_CLIENT_SECRET_FILE,
            scopes=[
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
                "openid"
            ],
            redirect_uri='postmessage'
        )
        session = requests.session()
        cached_session = CacheControl(session)
        self.request = google.auth.transport.requests.Request(
            session=cached_session
        )

    def generate_shelter_token(self, code: str) -> tuple[ShelterGoogleUser, str, str]:
        try:
            self.flow.fetch_token(code=code)
            credentials = self.flow.credentials

            payload = id_token.verify_oauth2_token(
                id_token=credentials._id_token,
                request=self.request,
                audience=GOOGLE_SHELTER_CLIENT_ID
            )

            user_data = ShelterGoogleUser(
                id=payload['sub'],
                email=payload['email'],
                name=payload['name'],
                picture=payload['picture'],
                given_name=payload['given_name'],
                family_name=payload['family_name']
            )

            return (user_data, credentials._id_token, credentials.refresh_token)
        except Exception as e:
            print(e)
            raise UnauthorizedError(e)

    def get_user_from_token(self, token: str) -> Union[ShelterGoogleUser, AdopterGoogleUser]:
        try:
            payload = id_token.verify_oauth2_token(
                id_token=token,
                request=self.request,
            )

            if payload['aud'] not in [GOOGLE_SHELTER_CLIENT_ID, GOOGLE_ADOPTER_CLIENT_ID]:
                raise UnauthorizedError('Could not verify client.')

            user_data = GoogleUser(
                id=payload['sub'],
                email=payload['email'],
                name=payload['name'] if 'name' in payload else None,
                picture=payload['picture'] if 'picture' in payload else None,
                given_name=payload['given_name'] if 'given_name' in payload else None,
                family_name=payload['family_name'] if 'family_name' in payload else None,
            )
            if payload['aud'] == GOOGLE_SHELTER_CLIENT_ID:
                user_data = ShelterGoogleUser(**user_data.model_dump())
            else:
                user_data = AdopterGoogleUser(**user_data.model_dump())

            return user_data
        except Exception as e:
            if isinstance(e, ValueError):
                raise UnauthorizedError('Expired token.')
            print(e)
            raise UnauthorizedError(e)

    def refresh_shelter_token(self, refresh_token: str) -> tuple[ShelterGoogleUser, str, str]:
        try:
            credentials = google.oauth2.credentials.Credentials(
                None,
                refresh_token=refresh_token,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=GOOGLE_SHELTER_CLIENT_ID,
                client_secret=GOOGLE_SHELTER_CLIENT_SECRET
            )

            credentials.refresh(self.request)

            payload = id_token.verify_oauth2_token(
                id_token=credentials.id_token,
                request=self.request,
                audience=GOOGLE_SHELTER_CLIENT_ID
            )

            user_data = ShelterGoogleUser(
                id=payload['sub'],
                email=payload['email'],
                name=payload['name'] if 'name' in payload else None,
                picture=payload['picture'] if 'picture' in payload else None,
                given_name=payload['given_name'] if 'given_name' in payload else None,
                family_name=payload['family_name'] if 'family_name' in payload else None,
            )

            return user_data, credentials.id_token, credentials.refresh_token
        except Exception as e:
            print(e)
            raise UnauthorizedError(e)
