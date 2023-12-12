from fastapi import APIRouter, Depends, HTTPException
from _common.exceptions import NotFoundException

from _common.response import GenericListResponse, GenericObjectResponse
from adopter.exceptions import AdopterAlreadyExists, AdopterNotFound
from adopter.model import Adopter
from adopter.service import AdopterService
from auth.dependencies import authenticate_adopter
from auth.models import AdopterGoogleUser
from ml_model.recommendation import RecommendationModel
from pet.model import PetResponse
from preference.model import AdopterPreference, CreateAdopterPreferenceRequestBody
from preference.service import AdopterPreferenceService
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


# @router.post("", response_model=GenericObjectResponse[Adopter])
# async def create_adopter(
#     body: CreateAdopterRequestBody,
#     user_context: AdopterGoogleUser = Depends(authenticate_adopter)
# ):
#     try:
#         service = AdopterService()
#         adopter = service.create_adopter(
#             name=user_context.name or "",
#             email=user_context.email,
#             bio=body.bio,
#             profile_picture=user_context.picture or ""
#         )
#         return GenericObjectResponse(
#             message="Created adopter successfully!",
#             data=adopter
#         )
#     except AdopterAlreadyExists:
#         raise HTTPException(
#             status_code=400,
#             detail="Adopter already exists."
#         )
#     except Exception as e:
#         print(e)
#         raise HTTPException(
#             status_code=500,
#             detail="Could not create adopter."
#         )


@router.post("/questionnaire", response_model=GenericObjectResponse[Questionnaire])
async def create_questionnaire(
    body: CreateQuestionnaire,
    user_context: AdopterGoogleUser = Depends(authenticate_adopter)
):
    try:
        service = AdopterService()
        adopter = service.create_adopter(
            id=user_context.id,
            name=user_context.name or "",
            email=user_context.email,
            profile_picture=user_context.picture or ""
        )

        service = QuestionnaireService()
        questionnaire = service.create_questionnaire(
            adopter=adopter,
            **body.model_dump()
        )
        return GenericObjectResponse(
            message="Created questionnaire successfully!",
            data=questionnaire
        )
    except AdopterAlreadyExists:
        raise HTTPException(
            status_code=400,
            detail="Adopter already exists."
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


@router.get("/me/preferences", response_model=GenericObjectResponse[Adopter])
async def get_adopter(user_context: AdopterGoogleUser = Depends(authenticate_adopter)):
    try:
        service = AdopterService()
        adopter = service.get_adopter_with_preferences(
            email=user_context.email
        )
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


@router.post("/me/preferences", response_model=GenericObjectResponse[AdopterPreference])
async def create_preferences(
    body: CreateAdopterPreferenceRequestBody,
    user_context: AdopterGoogleUser = Depends(authenticate_adopter)
):
    try:
        service = AdopterPreferenceService()
        preference = service.create_preference(
            adopter_id=user_context.id,
            **body.model_dump()
        )

        return GenericObjectResponse(
            message="Created preferences successfully!",
            data=preference
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
            detail="Could not create preferences."
        )


@router.get("/me/recommendations", response_model=GenericListResponse[PetResponse])
async def get_recommendations(
    user_context: AdopterGoogleUser = Depends(authenticate_adopter)
):
    try:
        service = AdopterService()
        adopter = service.get_adopter(
            id=user_context.id
        )

        model = RecommendationModel()
        recommendations = model.recommend(
            adopter=adopter
        )[:20]

        return GenericListResponse(
            message="Retrieved recommendations successfully!",
            data=[pet.to_response() for pet in recommendations]
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve recommendations."
        )
