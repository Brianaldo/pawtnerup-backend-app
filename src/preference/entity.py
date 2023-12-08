from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Enum
from sqlalchemy.orm import relationship, Mapped
from _infrastructure.database.base_model import Base
from preference.model import AdopterPreference, PreferenceEnum


class AdopterPreferenceEntity(Base):
    __tablename__ = "adopter_preferences"

    id = Column(Integer, primary_key=True)
    adopter_id = Column(String(30), ForeignKey("adopters.id", ondelete='CASCADE'),
                        nullable=False, index=True)
    adopter: Mapped["AdopterEntity"] = relationship(
        back_populates="preferences")
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete='CASCADE'),
                    nullable=False, index=True)
    pet: Mapped["PetEntity"] = relationship(back_populates="preferences")
    preference = Column(Enum(PreferenceEnum), nullable=False)
    __table_args__ = (UniqueConstraint('adopter_id', 'pet_id', name='_adopter_pet_uc'),
                      )

    def __repr__(self):
        return f"<AdopterPreference(adopter_id={self.adopter_id}, pet_id={self.pet_id}, preference={self.preference})>"

    def to_model(self) -> AdopterPreference:
        return AdopterPreference(
            pet_id=self.pet_id,
            pet=self.pet.to_model(),
            preference=self.preference
        )
