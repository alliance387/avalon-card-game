from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from .database import Base

class ModelApp(Base):
    __tablename__ = 'apps'
    id = Column(Integer, primary_key=True)
    access_key = Column(String)
    secret = Column(String)
    management_key = Column(String)
    template_id = Column(String)
    date_status = Column(Date)

    rooms = relationship('ModelRoom', back_populates='app')


class ModelRoom(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_id = Column(String)
    code = Column(String)

    app_id = Column(Integer, ForeignKey('apps.id'))

    sessions_in_room = relationship('ModelSession', back_populates='rooms_in_session')
    app = relationship('ModelApp', back_populates='rooms')


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
