from fastapi import APIRouter, Depends, HTTPException

from _common.response import GenericObjectResponse
from adopter.exceptions import AdopterAlreadyExists, AdopterNotFound
from adopter.model import Adopter, CreateAdopterRequestBody
from adopter.service import AdopterService
from auth.dependencies import authenticate_adopter
from auth.models import AdopterGoogleUser
from questionnaire.model import CreateQuestionnaire, Questionnaire
from questionnaire.service import QuestionnaireService


router = APIRouter(
    prefix="/adopters",
    tags=["adopters"]
)


@router.get("/me", response_model=GenericObjectResponse[Adopter])
async def get_adopter(user_context: AdopterGoogleUser = Depends(authenticate_adopter)):
    try:
        service = AdopterService()
        adopter = service.get_adopter(email=user_context.email)
        return GenericObjectResponse(
            message="Retrieved adopters successfully!",
            data=adopter
        )
    except AdopterNotFound:
        raise HTTPException(
            status_code=403,
            detail="Unregistered adopter."
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve adopters."
        )


@router.post("", response_model=GenericObjectResponse[Adopter])
async def create_adopter(
    body: CreateAdopterRequestBody,
    user_context: AdopterGoogleUser = Depends(authenticate_adopter)
):
    try:
        service = AdopterService()
        adopter = service.create_adopter(
            name=user_context.name or "",
            email=user_context.email,
            bio=body.bio,
            profile_picture=user_context.picture or ""
        )
        return GenericObjectResponse(
            message="Created adopter successfully!",
            data=adopter
        )
    except AdopterAlreadyExists:
        raise HTTPException(
            status_code=400,
            detail="Adopter already exists."
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not create adopter."
        )


@router.post("/questionnaire", response_model=GenericObjectResponse[Questionnaire])
async def create_questionnaire(
    body: CreateQuestionnaire,
    user_context: AdopterGoogleUser = Depends(authenticate_adopter)
):
    try:
        service = QuestionnaireService()
        questionnaire = service.create_questionnaire(
            adopter_email=user_context.email,
            **body.model_dump()
        )
        return GenericObjectResponse(
            message="Created questionnaire successfully!",
            data=questionnaire
        )
    except AdopterNotFound:
        raise HTTPException(
            status_code=403,
            detail="Unregistered adopter."
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not create questionnaire."
        )
