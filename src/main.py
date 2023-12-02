import os

from fastapi import FastAPI
from auth.router import router as auth_router
from shelter.router import router as shelter_router
from breed.router import router as breed_router
from pet.router import router as pet_router
from _infrastructure.database.engine import db_engine
from _infrastructure.database.base_model import Base

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = FastAPI()


@app.get("/")
async def root():
    return "PawtnerUP API v1"

app.include_router(auth_router)
app.include_router(shelter_router)
app.include_router(breed_router)
app.include_router(pet_router)

Base.metadata.create_all(db_engine)
