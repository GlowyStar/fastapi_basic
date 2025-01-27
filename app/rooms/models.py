from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Index
from sqlalchemy.orm import relationship


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)

    # Отношения
    hotel = relationship("Hotels", back_populates="rooms")
    bookings = relationship("Bookings", back_populates="room", cascade="all, delete-orphan")

    # Индексы
    __table_args__ = (
        Index("ix_rooms_hotel_id", "hotel_id"),
        Index("ix_rooms_name", "name"),
        Index("ix_rooms_price", "price"),
    )

    def __repr__(self):
        return (
            f"Rooms(id={self.id}, hotel_id={self.hotel_id}, name={self.name}, "
            f"description={self.description}, price={self.price}, services={self.services}, "
            f"quantity={self.quantity}, image_id={self.image_id})"
        )

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        return {
            "id": self.id,
            "hotel_id": self.hotel_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "services": self.services,
            "quantity": self.quantity,
            "image_id": self.image_id,
        }
