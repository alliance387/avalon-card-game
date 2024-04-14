from sqlalchemy.orm import Session


from .models import ModelRoom, ModelUser, ModelSession, ModelApp
from .schema import UserSchema, SessionSchema, RoomSchema, AppSchema

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
def get_all_rooms(db: Session):
    return db.query(ModelRoom).all()

def get_room_by_100ms_room_id(db: Session, ms100_room_id: str):
    return db.query(ModelRoom).filter(ModelRoom.room_id == ms100_room_id).first()

def get_room_by_room_code(db: Session, room_code: str):
    return db.query(ModelRoom).filter(ModelRoom.code == room_code).first()

def create_room(db: Session, room: RoomSchema):
    db_room = ModelRoom(room_id = room.room_id, code = room.code, app_id= room.app_id)
    db.add(db_room)
    db.commit()
    return db_room

# app part
def create_app(db: Session, app: AppSchema):
    db_app = ModelApp(access_key = app.access_key, secret = app.secret, management_key = app.management_key, template_id = app.template_id, date_status = app.date_status)
    db.add(db_app)
    db.commit()
    return db_app

def get_all_apps(db: Session):
    return db.query(ModelApp).all()

def get_app_by_access_key(db: Session, access_key: str):
    return db.query(ModelApp).filter(ModelApp.access_key == access_key).first()

def update_app_management_key(db: Session, app_id: int, management_key: str, date: str):
    db_app = db.query(ModelApp).filter(ModelApp.id == app_id).first()
    db_app.management_key = management_key
    db_app.date_status = date
    db.commit()
    return management_key

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item