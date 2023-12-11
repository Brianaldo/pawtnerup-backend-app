import enum
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, backref
from _infrastructure.database import Base
from breed.model import BreedSizeEnum
from pet.model import AgeEnum, GenderEnum
from questionnaire.model import Questionnaire


class QuestionnaireEntity(Base):
    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True)
    adopter_id = Column(String(50), ForeignKey(
        "adopters.id", ondelete='CASCADE'), unique=True)
    adopter: Mapped["AdopterEntity"] = relationship(
        back_populates="questionnaire")
    pet_sizes: Mapped[list["PetSizeQuestionnaireEntity"]] = relationship(
        back_populates="questionnaire")
    pet_ages: Mapped[list["PetAgeQuestionnaireEntity"]] = relationship(
        back_populates="questionnaire")
    pet_genders: Mapped[list["PetGenderQuestionnaireEntity"]] = relationship(
        back_populates="questionnaire")
    breeds: Mapped[list["BreedQuestionnaireEntity"]] = relationship(
        back_populates="questionnaire")

    def to_model(self) -> Questionnaire:
        return Questionnaire(
            id=self.id,
            adopter_id=self.adopter_id,
            adopter=self.adopter.to_model(),
            pet_sizes=list(map(lambda size: size.answer, self.pet_sizes)),
            pet_ages=list(map(lambda age: age.answer, self.pet_ages)),
            pet_genders=list(
                map(lambda gender: gender.answer, self.pet_genders)),
            breeds=list(map(lambda breed: breed.breed.name, self.breeds))
        )


class PetSizeQuestionnaireEntity(Base):
    __tablename__ = "pet_size_questionnaires"

    id = Column(Integer, primary_key=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"))
    questionnaire: Mapped["QuestionnaireEntity"] = relationship(
        back_populates="pet_sizes")
    answer = Column(Enum(BreedSizeEnum))


class PetAgeQuestionnaireEntity(Base):
    __tablename__ = "pet_age_questionnaires"

    id = Column(Integer, primary_key=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"))
    questionnaire: Mapped["QuestionnaireEntity"] = relationship(
        back_populates="pet_ages")
    answer = Column(Enum(AgeEnum))


class PetGenderQuestionnaireEntity(Base):
    __tablename__ = "pet_gender_questionnaires"

    id = Column(Integer, primary_key=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"))
    questionnaire: Mapped["QuestionnaireEntity"] = relationship(
        back_populates="pet_genders")
    answer = Column(Enum(GenderEnum))


class BreedQuestionnaireEntity(Base):
    __tablename__ = "breed_questionnaires"

    id = Column(Integer, primary_key=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"))
    questionnaire: Mapped["QuestionnaireEntity"] = relationship(
        back_populates="breeds")
    breed_id = Column(Integer, ForeignKey("breeds.id"))
    breed: Mapped["BreedEntity"] = relationship(
        back_populates="questionnaires")
