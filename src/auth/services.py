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


flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    client_secrets_file=SHELTER_CLIENT_SECRET_FILE,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_uri='postmessage'
)


def get_shelter_authorization_url() -> tuple:
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    return authorization_url, state


def generate_shelter_token(code: str) -> tuple[ShelterGoogleUser, str, str]:
    try:
        flow.fetch_token(code=code, )
        credentials = flow.credentials

        session = requests.session()
        cached_session = CacheControl(session)
        request = google.auth.transport.requests.Request(
            session=cached_session
        )

        payload = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=request,
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
    except ValueError:
        raise UnauthorizedError('Could not verify token.')


def get_user_from_token(token: str) -> Union[ShelterGoogleUser, AdopterGoogleUser]:
    try:
        session = requests.session()
        cached_session = CacheControl(session)
        request = google.auth.transport.requests.Request(
            session=cached_session
        )

        payload = id_token.verify_oauth2_token(
            id_token=token,
            request=request,
        )

        if payload['aud'] not in [GOOGLE_SHELTER_CLIENT_ID, GOOGLE_ADOPTER_CLIENT_ID]:
            raise UnauthorizedError('Could not verify client.')

        user_data = GoogleUser(
            id=payload['sub'],
            email=payload['email'],
            name=payload['name'],
            picture=payload['picture'],
            given_name=payload['given_name'],
            family_name=payload['family_name'],
        )
        if payload['aud'] == GOOGLE_SHELTER_CLIENT_ID:
            user_data = ShelterGoogleUser(**user_data.model_dump())
        else:
            user_data = AdopterGoogleUser(**user_data.model_dump())

        return user_data
    except ValueError:
        raise UnauthorizedError('Could not verify token.')


def refresh_shelter_token(refresh_token: str) -> tuple[ShelterGoogleUser, str, str]:
    try:
        credentials = google.oauth2.credentials.Credentials(
            None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=GOOGLE_SHELTER_CLIENT_ID,
            client_secret=GOOGLE_SHELTER_CLIENT_SECRET
        )

        request = google.auth.transport.requests.Request()
        credentials.refresh(request)

        session = requests.session()
        cached_session = CacheControl(session)
        request = google.auth.transport.requests.Request(
            session=cached_session
        )

        payload = id_token.verify_oauth2_token(
            id_token=credentials.id_token,
            request=request,
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

        return user_data, credentials.id_token, credentials.refresh_token
    except ValueError:
        raise UnauthorizedError('Could not refresh token.')
