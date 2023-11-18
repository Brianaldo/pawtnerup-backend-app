import os
import pathlib
import json

"""
Google OAuth 2.0 Configuration for Adopter Client
"""
GOOGLE_ADOPTER_CLIENT_ID = ""


"""
Google OAuth 2.0 Configuration for Shelter Client
"""
SHELTER_CLIENT_SECRET_FILE = os.path.join(
    pathlib.Path(__file__).parent.parent.parent, "storage/shelter_client_secret.json")
SHELTER_CLIENT_REDIRECT_URI = "http://localhost:8000/auth/shelter/callback"

with open(SHELTER_CLIENT_SECRET_FILE) as f:
    data = json.load(f)
    GOOGLE_SHELTER_CLIENT_ID = data["web"]["client_id"]
    GOOGLE_SHELTER_CLIENT_SECRET = data["web"]["client_secret"]
