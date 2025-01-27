from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Date, Computed, Index
from sqlalchemy.orm import relationship

class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)

    # Вычисляемые поля
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
    total_days = Column(Integer, Computed("(date_to - date_from)"))

    # Отношения
    room = relationship("Rooms", back_populates="bookings")
    user = relationship("Users", back_populates="bookings")

    # Индексы
    __table_args__ = (
        Index("ix_bookings_user_id", "user_id"),
        Index("ix_bookings_date_from", "date_from"),
    )

    # Методы представления
    def __repr__(self):
        return (
            f"Bookings(id={self.id}, room_id={self.room_id}, user_id={self.user_id}, "
            f"date_from={self.date_from}, date_to={self.date_to}, price={self.price}, "
            f"total_cost={self.total_cost}, total_days={self.total_days})"
        )

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "user_id": self.user_id,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "price": self.price,
            "total_cost": self.total_cost,
            "total_days": self.total_days,
        }
