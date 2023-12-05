from _infrastructure.database.base_repository import BaseRepository
from adopter.entity import AdopterEntity
from adopter.model import Adopter
from questionnaire.entities import BreedQuestionnaireEntity, PetAgeQuestionnaireEntity, PetGenderQuestionnaireEntity, PetPersonalityQuestionnaireEntity, PetSizeQuestionnaireEntity, QuestionnaireEntity
from questionnaire.model import QuestionnaireTyped


class QuestionnaireRepository(BaseRepository[QuestionnaireTyped, QuestionnaireEntity]):
    def __init__(self):
        super().__init__(QuestionnaireEntity)

    def create(self, adopter: Adopter, **kwargs: QuestionnaireTyped) -> QuestionnaireEntity:
        try:
            adopter_entity = self.session.merge(AdopterEntity(
                **adopter.model_dump(exclude_unset=True)
            ))

            personality_entity = PetPersonalityQuestionnaireEntity(
                answer=kwargs.get("pet_personality")
            )

            pet_size_entities = [
                PetSizeQuestionnaireEntity(answer=size)
                for size in kwargs.get("pet_sizes")
            ]

            pet_age_entities = [
                PetAgeQuestionnaireEntity(answer=age)
                for age in kwargs.get("pet_ages")
            ]

            pet_gender_entities = [
                PetGenderQuestionnaireEntity(answer=gender)
                for gender in kwargs.get("pet_genders")
            ]

            breed_entities = [
                self.session.merge(BreedQuestionnaireEntity(breed_id=breed_id))
                for breed_id in kwargs.get("breed_ids")
            ]

            record = QuestionnaireEntity(
                adopter=adopter_entity,
                pet_personality=personality_entity,
                pet_sizes=pet_size_entities,
                pet_ages=pet_age_entities,
                pet_genders=pet_gender_entities,
                breeds=breed_entities
            )
            self.session.add(record)
            self.session.commit()
            return record
        except Exception as e:
            print("QuestionnaireRepository::create: ", e)
            self.session.rollback()
            raise e
