from typing import TypedDict
from sqlalchemy import Column, Integer, String
from _infrastructure.database import Base


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    address = Column(String(50))
    phone_number = Column(String(50))

    def __repr__(self):
        return f"<Shelter(id={self.id}, name={self.name}, email={self.email}, address={self.address}, phone_number={self.phone_number})>"


class ShelterDict(TypedDict, total=False):
    id: int
    name: str
    email: str
    address: str
    phone_number: str
