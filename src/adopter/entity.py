from sqlalchemy import Column, Integer, String
from _infrastructure.database.base_model import Base
from adopter.model import Adopter
from sqlalchemy.orm import relationship, Mapped


class AdopterEntity(Base):
    __tablename__ = "adopters"

    id = Column(String(30), primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    profile_picture = Column(String(200))
    questionnaire: Mapped["QuestionnaireEntity"] = relationship(
        back_populates="adopter", cascade='all, delete')
    preferences: Mapped[list["AdopterPreferenceEntity"]] = relationship(
        back_populates="adopter", cascade='all, delete')

    def to_model(self) -> Adopter:
        return Adopter(
            id=self.id,
            name=self.name,
            email=self.email,
            profile_picture=self.profile_picture,
            preferences=None,
        )

    def to_model_with_preferences(self) -> Adopter:
        return Adopter(
            id=self.id,
            name=self.name,
            email=self.email,
            profile_picture=self.profile_picture,
            preferences=list(
                map(lambda pref: pref.to_model(), self.preferences)),
        )

    def __repr__(self):
        return f"<Adopter(id={self.id}, name={self.name}, email={self.email}, bio={self.bio})>"
