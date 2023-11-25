import os

from fastapi import FastAPI
from auth.routers import router as auth_router
from shelter.router import router as shelter_router

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)
app.include_router(shelter_router)
