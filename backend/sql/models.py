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
    games = relationship('ModelGame', back_populates='room')


class ModelUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    sessions_in_user = relationship('ModelSession', back_populates='users_in_session')
    active_in_lobbies = relationship('ModelActiveUser', back_populates='user')


class ModelSession(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))

    users_in_session = relationship('ModelUser', back_populates='sessions_in_user')
    rooms_in_session = relationship('ModelRoom', back_populates='sessions_in_room')


class ModelGame(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    good_win = Column(Integer, default=0)
    evil_win = Column(Integer, default=0)
    rejected_rounds = Column(Integer, default=0)
    win = Column(Integer, default=0)
    room_id = Column(Integer, ForeignKey('rooms.id'))

    room = relationship('ModelRoom', back_populates='games')
    active_users = relationship('ModelActiveUser', back_populates='game')


class ModelActiveUser(Base):
    __tablename__ = 'activeUsers'
    id = Column(Integer, primary_key=True)
    role = Column(String, default='guest')
    user_id = Column(Integer, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))

    user = relationship('ModelUser', back_populates='active_in_lobbies')
    game = relationship('ModelGame', back_populates='active_users')


