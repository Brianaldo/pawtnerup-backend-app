import os

from fastapi import FastAPI
from auth.router import router as auth_router

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)
