from sqlalchemy import Column, Integer, String
from _infrastructure.database import Base
# from pet.entity import PetEntity
from shelter.model import Shelter
from sqlalchemy.orm import relationship, Mapped


class ShelterEntity(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    contact_email = Column(String(50))
    address = Column(String(50))
    phone_number = Column(String(50))

    pets: Mapped[list["PetEntity"]] = relationship(back_populates="shelter")

    def to_model(self) -> Shelter:
        return Shelter(
            id=self.id,
            name=self.name,
            email=self.email,
            contact_email=self.contact_email,
            address=self.address,
            phone_number=self.phone_number,
        )

    def __repr__(self):
        return f"<Shelter(id={self.id}, name={self.name}, email={self.email}, address={self.address}, phone_number={self.phone_number})>"
