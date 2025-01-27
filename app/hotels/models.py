from app.database import Base
from sqlalchemy import Column, Integer, String, JSON, Index
from sqlalchemy.orm import relationship


class Hotels(Base):
    __tablename__ = "hotels"

    # Поля таблицы
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON, nullable=False)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)

    # Отношения
    rooms = relationship("Rooms", back_populates="hotel", cascade="all, delete-orphan")

    # Индексы
    __table_args__ = (
        Index("ix_hotels_name", "name"),
        Index("ix_hotels_location", "location"),
    )

    # Методы представления
    def __repr__(self):
        return (
            f"Hotels(id={self.id}, name={self.name}, location={self.location}, "
            f"services={self.services}, rooms_quantity={self.rooms_quantity}, image_id={self.image_id})"
        )

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "services": self.services,
            "rooms_quantity": self.rooms_quantity,
            "image_id": self.image_id,
        }
