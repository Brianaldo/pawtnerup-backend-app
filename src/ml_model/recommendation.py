from adopter.model import Adopter
from ml_model.collaborative_filtering import CollaborativeFilteringModel, InputAdopter
from ml_model.content_based_filtering import ContentBasedFilteringModel, InputData
from pet.model import Pet
from preference.repository import AdopterPreferenceRepository
from questionnaire.repository import QuestionnaireRepository


class RecommendationModel:
    def __init__(self):
        self.questionnaire_repository = QuestionnaireRepository()
        self.preference_repository = AdopterPreferenceRepository()
        self.content_based_model = ContentBasedFilteringModel()
        self.collaborative_filtering_model = CollaborativeFilteringModel()

    def recommend(self, adopter: Adopter) -> list[Pet]:
        adopter_questionnaire = self.questionnaire_repository.get_one_by_filter(
            adopter_id=adopter.id).to_model()
        similar_adopter = self.collaborative_filtering_model.get_most_similar(
            InputAdopter(
                gender=adopter_questionnaire.pet_genders,
                age=adopter_questionnaire.pet_ages,
                breed=adopter_questionnaire.breeds
            )
        )

        gender = set(adopter_questionnaire.pet_genders)
        gender.add(similar_adopter.gender)
        gender = list(gender)

        age = set(adopter_questionnaire.pet_ages)
        age.add(similar_adopter.age)
        age = list(age)

        breed = set(adopter_questionnaire.breeds)
        breed.add(similar_adopter.breed)
        breed = list(breed)

        pet_recommendation = self.content_based_model.get_most_similar(
            InputData(
                gender=gender,
                age=age,
                breed=breed
            )
        )

        adopter_past_preferences = list(map(lambda x: x.to_model(), self.preference_repository.get_by_filter(
            adopter_id=adopter.id)))
        past_pet_id = [
            preference.pet_id for preference in adopter_past_preferences]

        pet_recommendation = [
            pet for pet in pet_recommendation if pet.id not in past_pet_id]

        return pet_recommendation
