from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.types import String, Boolean

class Base(DeclarativeBase):
    pass 

class Pet(Base):
    __tablename__ = 'pets'
    id: Mapped[Integer] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[String] = Column(String(100), nullable=False)
    species: Mapped[String] = Column(String(100), nullable=False)
    photo_url: Mapped[String | None] = Column(String(1000))
    age: Mapped[Integer | None] = Column(Integer)
    notes: Mapped[String | None] = Column(String(length=1000))
    available: Mapped[Boolean] = Column(Boolean, nullable=False, default=True)
    
