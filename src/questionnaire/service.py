from adopter.repository import AdopterRepository
from adopter.service import AdopterService
from questionnaire.model import Questionnaire, QuestionnaireTyped
from questionnaire.repository import QuestionnaireRepository


class QuestionnaireService:
    def __init__(self):
        self.questionnaire_repository = QuestionnaireRepository()
        self.adopter_service = AdopterService()

    def create_questionnaire(self, adopter_email: str, **kwargs: QuestionnaireTyped) -> Questionnaire:
        adopter = self.adopter_service.get_adopter(
            email=adopter_email
        )
        return self.questionnaire_repository.create(adopter=adopter, **kwargs).to_model()
