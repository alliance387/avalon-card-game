from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base  = declarative_base()


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_id = Column(String)
    code = Column(String)