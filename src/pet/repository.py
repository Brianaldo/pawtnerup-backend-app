from _infrastructure.database.base_repository import BaseRepository
from breed.entity import BreedEntity
from pet.entity import PetEntity
from pet.model import PetTyped
from shelter.entity import ShelterEntity
from shelter.exceptions import ShelterNotFound


class PetRepository(BaseRepository[PetTyped, PetEntity]):
    def __init__(self):
        super().__init__(PetEntity)

    def create(self, shelter_email: str, **kwargs: PetTyped) -> PetEntity:
        shelter = self.session.query(ShelterEntity).filter(
            ShelterEntity.email == shelter_email
        ).first()
        if shelter is None:
            raise ShelterNotFound("Shelter not found")

        breed = self.session.query(BreedEntity).filter(
            BreedEntity.name == kwargs.get('breed')
        ).first()
        if breed is None:
            breed_name: str = kwargs.get('breed')
            breed = BreedEntity(name=breed_name.lower())
            self.session.add(breed)

        kwargs["breed"] = breed
        kwargs["shelter"] = shelter
        record = PetEntity(**kwargs)
        self.session.add(record)
        self.session.commit()
        return record

    def fetch_by_shelter(self, shelter_email: str) -> list[PetEntity]:
        shelter = self.session.query(ShelterEntity).filter(
            ShelterEntity.email == shelter_email
        ).first()
        if shelter is None:
            raise ShelterNotFound("Shelter not found")
        return self.session.query(PetEntity).filter(
            PetEntity.shelter == shelter
        ).all()
