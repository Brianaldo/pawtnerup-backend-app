from adopter.repository import AdopterRepository
from adopter.service import AdopterService
from questionnaire.model import Questionnaire, QuestionnaireTyped
from questionnaire.repository import QuestionnaireRepository


class QuestionnaireService:
    def __init__(self):
        self.questionnaire_repository = QuestionnaireRepository()
        self.adopter_service = AdopterService()

    def create_questionnaire(self, **kwargs: QuestionnaireTyped) -> Questionnaire:
        return self.questionnaire_repository.create(**kwargs).to_model()
