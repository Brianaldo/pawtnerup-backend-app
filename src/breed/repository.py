from _infrastructure.database.base_repository import BaseRepository
from breed.entity import BreedEntity
from breed.exception import BreedNotFound
from breed.model import BreedTyped


class BreedRepository(BaseRepository[BreedTyped, BreedEntity]):
    def __init__(self):
        super().__init__(BreedEntity)

    def get_by_filter(self, **kwargs: BreedTyped) -> list[BreedEntity]:
        id = kwargs.get('id')
        name = kwargs.get('name')
        return self.session.query(BreedEntity).filter(
            BreedEntity.id == id if id is not None else True,
            BreedEntity.name.ilike(
                "%{}%".format(name)
            ) if name is not None else True,
            BreedEntity.size.in_(kwargs.get('size')) if kwargs.get(
                'size') is not None else True,
        ).all()

    def get_one_by_filter(self, **kwargs: BreedTyped) -> BreedEntity:
        id = kwargs.get('id')
        name = kwargs.get('name')
        breed = self.session.query(BreedEntity).filter(
            BreedEntity.id == id if id is not None else True,
            BreedEntity.name.ilike(
                "%{}%".format(name)
            ) if name is not None else True,
        ).first()

        if breed is None:
            raise BreedNotFound("Breed not found")

        return breed
