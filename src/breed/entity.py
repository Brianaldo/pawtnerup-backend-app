from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from _infrastructure.database.base_model import Base
from breed.model import Breed

# from pet.entity import PetEntity


class BreedEntity(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    pets: Mapped[list["PetEntity"]] = relationship(back_populates="breed")

    def to_model(self) -> Breed:
        return Breed(
            id=self.id,
            name=self.name,
        )

    def __repr__(self):
        return f"<Breed(id={self.id}, name={self.name})>"
