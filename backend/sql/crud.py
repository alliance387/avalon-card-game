from sqlalchemy.orm import Session


from .models import ModelRoom, ModelUser, ModelSession
from .schema import UserSchema, SessionSchema, RoomSchema

# user part
def get_user(db: Session, user_id: int):
    return db.query(ModelUser).filter(ModelUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(ModelUser).filter(ModelUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ModelUser).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserSchema, hashed_password: str):
    db_user = ModelUser(full_name = user.full_name, email = user.email, password = hashed_password)
    db.add(db_user)
    db.commit()
    return db_user


# session part
def get_sessions_by_user(db: Session, user: UserSchema):
    return db.query(ModelSession).filter(ModelSession.user_id == user.id).all()

def get_sessions_by_room(db: Session, room: RoomSchema):
    return db.query(ModelSession).filter(ModelSession.room_id == room.id).all()

def create_session(db: Session, session: SessionSchema):
    db_session = ModelSession(user_id = session.user_id, room_id = session.room_id)
    db.add(db_session)
    db.commit()
    return db_session

# room part
def get_room_by_100ms_room_id(db: Session, ms100_room_id: str):
    return db.query(ModelRoom).filter(ModelRoom.room_id == ms100_room_id).first()

def create_room(db: Session, room: RoomSchema):
    db_room = ModelRoom(room_id = room.room_id, code = room.code)
    db.add(db_room)
    db.commit()
    return db_room

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item