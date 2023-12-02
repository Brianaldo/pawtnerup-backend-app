import os
import pathlib
import json

"""
Google OAuth 2.0 Configuration for Adopter Client
"""
ADOPTER_CLIENT_SECRET_FILE = os.path.join(
    pathlib.Path(__file__).parent.parent.parent, "storage/adopter_client_secret.json")

with open(ADOPTER_CLIENT_SECRET_FILE) as f:
    data = json.load(f)
    GOOGLE_ADOPTER_CLIENT_ID = data["installed"]["client_id"]


"""
Google OAuth 2.0 Configuration for Shelter Client
"""
SHELTER_CLIENT_SECRET_FILE = os.path.join(
    pathlib.Path(__file__).parent.parent.parent, "storage/shelter_client_secret.json")

with open(SHELTER_CLIENT_SECRET_FILE) as f:
    data = json.load(f)
    GOOGLE_SHELTER_CLIENT_ID = data["web"]["client_id"]
    GOOGLE_SHELTER_CLIENT_SECRET = data["web"]["client_secret"]
