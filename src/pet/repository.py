from _infrastructure.database.base_repository import BaseRepository
from _infrastructure.database.exceptions import NotFoundError
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

    def update(self, pet_id: int, shelter_email: str, **kwargs: PetTyped) -> PetEntity:
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

        record = self.session.query(PetEntity).filter(
            PetEntity.id == pet_id,
            PetEntity.shelter == shelter
        ).first()
        if record is None:
            raise NotFoundError('Record not found')

        for key, value in kwargs.items():
            setattr(record, key, value)

        self.session.commit()
        return record
