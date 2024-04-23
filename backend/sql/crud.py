from sqlalchemy.orm import Session


from .models import ModelRoom, ModelUser, ModelSession, ModelApp, ModelGame, ModelActiveUser
from .schema import UserSchema, SessionSchema, RoomSchema, AppSchema, GameSchema, ActiveUserSchema

# user part
def get_all_users(db: Session):
    return db.query(ModelUser).all()


def get_user(db: Session, user_id: int):
    return db.query(ModelUser).filter(ModelUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(ModelUser).filter(ModelUser.email == email).first()


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


def get_session_by_room_and_user(db: Session, user_id: int, room_id: int):
    return db.query(ModelSession).filter(ModelSession.user_id == user_id, ModelSession.room_id == room_id).first()


def delete_session_crud(db: Session, user_id: int, room_id: int):
    db_session = db.query(ModelSession).filter(ModelSession.user_id == user_id, ModelSession.room_id == room_id).first()
    db.delete(db_session)
    db.commit()
    return get_session_by_room_and_user(db, user_id, room_id)


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


# game part
def create_game(db: Session, number: int, room_id: int):
    db_game = ModelGame(number = number, room_id = room_id)
    db.add(db_game)
    db.commit()
    return db_game


def get_game_by_id(db: Session, game_id: int):
    return db.query(ModelGame).filter(ModelGame.id == game_id).first()


def get_game_by_room_id(db: Session, room_id: int):
    return db.query(ModelGame).filter(ModelGame.room_id == room_id).first()


def update_room(db: Session, game_id: int, elements_to_change: dict[str, int]):
    db_game = db.query(ModelGame).filter(ModelGame.id == game_id).first()

    if elements_to_change.get('evil_win') or elements_to_change.get('good_win'):
        db_game.good_win += int(elements_to_change.get('good_win', 0))
        db_game.evil_win += int(elements_to_change.get('evil_win', 0))
        db_game.rejected_rounds = 0
    else:
        db_game.rejected_rounds += elements_to_change.get('rejected_rounds', 0)
    
    db.commit()
    return db_game


def update_room_status(db: Session, game_id: int, win: int):
    db_game = db.query(ModelGame).filter(ModelGame.id == game_id).first()
    db_game.win = win
    db.commit()
    return db_game


# active users part
def create_active_users(db: Session, game_id: int, users: dict[str, object]):
    for value in users.values():
        db_user = db.query(ModelUser).filter(ModelUser.email == value['name']).first()
        db_game = ModelActiveUser(role = value['role'], user_id = db_user.id, game_id = game_id, order = value['order'], mermaid = value['mermaid'])
        db.add(db_game)
    db.commit()
    return db.query(ModelGame).filter(ModelGame.id == game_id).first().active_users


def get_active_user(db: Session, game_id: int, user_id: int):
    return db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.user_id == user_id).first()

def get_active_users(db: Session, game_id: int):
    return db.query(ModelActiveUser).all()

def update_active_user_mermaid(db: Session, game_id: int, user_id: int):
    db_user = db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.mermaid == 1).first()
    db_user.mermaid = 2
    db_new_mermaid = db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.user_id == user_id).first()
    db_new_mermaid.mermaid = 1
    db.commit()
    return db_new_mermaid.role, db_user.email
