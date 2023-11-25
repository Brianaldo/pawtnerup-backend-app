from _infrastructure.database.base_model import Base
from _infrastructure.database.engine import db_engine
from typing import Type, TypeVar, Generic, TypedDict
from sqlalchemy.orm import sessionmaker

T = TypeVar('T', bound=TypedDict)
M = TypeVar('M', bound=Base)


class BaseRepository(Generic[T, M]):
    def __init__(self, model: Type[M]):
        Base.metadata.create_all(db_engine)
        self.model = model
        Session = sessionmaker(bind=db_engine)
        self.session = Session()

    def create(self, **kwargs: T) -> M:
        record = self.model(**kwargs)
        self.session.add(record)
        self.session.commit()
        return record

    def get_by_filter(self, **kwargs: T) -> list[M]:
        return self.session.query(self.model).filter_by(**kwargs).all()

    def get_one_by_filter(self, **kwargs: T) -> M:
        return self.session.query(self.model).filter_by(**kwargs).first()

    def update(self, id, **kwargs: T) -> M:
        record = self.session.query(self.model).get(id)
        for key, value in kwargs.items():
            setattr(record, key, value)
        self.session.commit()
        return record

    def delete(self, id) -> None:
        record = self.session.query(self.model).get(id)
        self.session.delete(record)
        self.session.commit()
