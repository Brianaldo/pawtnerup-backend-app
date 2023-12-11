from urllib.parse import urlencode as encode_query_string
from urllib.parse import parse_qs as parse_query_string
from starlette.types import ASGIApp, Scope, Receive, Send
import os

from fastapi import FastAPI
from auth.router import router as auth_router
from shelter.router import router as shelter_router
from adopter.router import router as adopter_router
from breed.router import router as breed_router
from pet.router import router as pet_router
from _infrastructure.database.engine import db_engine
from _infrastructure.database.base_model import Base
from fastapi.middleware.cors import CORSMiddleware

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class QueryStringFlatteningMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        query_string = scope.get("query_string", None).decode()
        if scope["type"] == "http" and query_string:
            parsed = parse_query_string(query_string)
            flattened = {}
            for name, values in parsed.items():
                all_values = []
                for value in values:
                    all_values.extend(value.split(","))

                flattened[name] = all_values

            # doseq: Turn lists into repeated parameters, which is better for FastAPI
            scope["query_string"] = encode_query_string(
                flattened, doseq=True).encode("utf-8")

            await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(QueryStringFlatteningMiddleware)


@app.get("/")
async def root():
    return "PawtnerUP API v1"

app.include_router(auth_router)
app.include_router(shelter_router)
app.include_router(adopter_router)
app.include_router(breed_router)
app.include_router(pet_router)

Base.metadata.create_all(db_engine)
