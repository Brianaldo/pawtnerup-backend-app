from _infrastructure.database.exceptions import AlreadyExistsError, NotFoundError
from adopter.exceptions import AdopterAlreadyExists, AdopterNotFound
from adopter.model import Adopter, AdopterTyped
from adopter.repository import AdopterRepository


class AdopterService():
    def __init__(self):
        self.adopter_repo = AdopterRepository()

    def get_adopter(self, **kwargs: AdopterTyped) -> Adopter:
        try:
            adopter = self.adopter_repo.get_one_by_filter(**kwargs)
            return adopter.to_model()
        except NotFoundError:
            raise AdopterNotFound('Adopter not found.')
        except Exception as e:
            print("AdopterService::get_adopter: ", e)
            raise e

    def create_adopter(self, **kwargs: AdopterTyped) -> Adopter:
        try:
            return self.adopter_repo.create(**kwargs).to_model()
        except AlreadyExistsError:
            raise AdopterAlreadyExists('Adopter already exists.')
        except Exception as e:
            print("AdopterService::create_adopter: ", e)
            raise e

    def get_adopter_with_preferences(self, **kwargs: AdopterTyped) -> Adopter:
        try:
            adopter = self.adopter_repo.get_one_by_filter(**kwargs)
            return adopter.to_model_with_preferences()
        except NotFoundError:
            raise AdopterNotFound('Adopter not found.')
        except Exception as e:
            print("AdopterService::get_adopter_with_preferences: ", e)
            raise e
