from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class ModelRoom(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_id = Column(String)
    code = Column(String)

    sessions_in_room = relationship('ModelSession', back_populates='rooms_in_session')


class ModelUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    sessions_in_user = relationship('ModelSession', back_populates='users_in_session')

class ModelSession(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))

    users_in_session = relationship('ModelUser', back_populates='sessions_in_user')
    rooms_in_session = relationship('ModelRoom', back_populates='sessions_in_room')
