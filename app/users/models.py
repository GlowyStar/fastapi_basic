from app.database import Base
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    # Поля таблицы
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    # Отношения
    bookings = relationship("Bookings", back_populates="user", cascade="all, delete-orphan")

    # Индексы
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
    )

    # Методы представления
    def __repr__(self):
        return f"Users(id={self.id}, email={self.email})"

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
        }
