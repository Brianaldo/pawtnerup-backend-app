from sqlalchemy import ARRAY, Column, Date, ForeignKey, Integer, String, Enum, Text
from _infrastructure.database import Base
from _infrastructure.object_storage.configs import CLOUD_STORAGE_BUCKET
# from breed.entity import BreedEntity
from pet.model import GenderEnum, Pet, SterilizationEnum
# from shelter.entity import ShelterEntity
from sqlalchemy.orm import relationship, Mapped


class PetEntity(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    gender = Column(Enum(GenderEnum))
    born_date = Column(Date())
    sterilization_status = Column(Enum(SterilizationEnum))
    rescue_story = Column(Text, nullable=True)
    media = Column(ARRAY(String), default=[])

    shelter_id = Column(Integer, ForeignKey("shelters.id"))
    shelter: Mapped["ShelterEntity"] = relationship(back_populates="pets")
    breed_id = Column(Integer, ForeignKey("breeds.id"))
    breed: Mapped["BreedEntity"] = relationship(back_populates="pets")

    def to_model(self) -> Pet:
        return Pet(
            id=self.id,
            name=self.name,
            gender=self.gender,
            shelter_id=self.shelter_id,
            breed=self.breed.name,
            born_date=self.born_date,
            sterilization_status=self.sterilization_status,
            rescue_story=self.rescue_story,
            media=map(
                lambda url: "https://storage.googleapis.com/{}/{}".format(CLOUD_STORAGE_BUCKET, url), self.media),
        )
