from _infrastructure.database.base_model import Base
from _infrastructure.database.engine import db_engine
from typing import Type, TypeVar, Generic, TypedDict
from sqlalchemy.orm import Session, sessionmaker

T = TypeVar('T', bound=TypedDict)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[Base]):
        Base.metadata.create_all(db_engine)
        self.model = model
        Session = sessionmaker(bind=db_engine)
        self.session = Session()

    def create(self, **kwargs: T) -> T:
        record = self.model(**kwargs)
        self.session.add(record)
        self.session.commit()
        return record

    def get_by_filter(self, **kwargs: T) -> list[T]:
        return self.session.query(self.model).filter_by(**kwargs).all()

    def get_one_by_filter(self, **kwargs: T) -> T:
        return self.session.query(self.model).filter_by(**kwargs).first()

    def update(self, id, **kwargs: T) -> T:
        record = self.session.query(self.model).get(id)
        for key, value in kwargs.items():
            setattr(record, key, value)
        self.session.commit()
        return record

    def delete(self, id) -> None:
        record = self.session.query(self.model).get(id)
        self.session.delete(record)
        self.session.commit()
