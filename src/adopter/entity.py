from sqlalchemy import Column, Integer, String
from _infrastructure.database.base_model import Base
from adopter.model import Adopter


class AdopterEntity(Base):
    __tablename__ = "adopters"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    bio = Column(String(100))

    def to_model(self) -> Adopter:
        return Adopter(
            id=self.id,
            name=self.name,
            email=self.email,
            bio=self.bio,
        )

    def __repr__(self):
        return f"<Adopter(id={self.id}, name={self.name}, email={self.email}, bio={self.bio})>"
