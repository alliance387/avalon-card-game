from sqlalchemy.orm import Session

import sql.models as models

def create_element_in_db(
        db: Session,
        model: str,
        params: dict
    ):
    new_db_element = getattr(models, model)(**params)
    db.add(new_db_element)
    db.commit()
    return new_db_element


def read_from_db(
        db: Session,
        model: str,
        params: dict,
        is_first: bool
    ):
    if not any(value for value in params.values()):
        elements = db.query(getattr(models, model)).all()
    else:
        elements = db.query(getattr(models, model)).filter(*(getattr(getattr(models, model), key) == value for key, value in params.items() if value)).all()

    if not elements:
        return None
    return elements[0] if is_first else elements


def update_from_db(
        db: Session,
        model: str,
        params: dict,
        params_to_change: dict
    ):
    elements = db.query(getattr(models, model)).filter(*(getattr(getattr(models, model), key) == value for key, value in params.items() if value)).first()
    for name, value in params_to_change.items():
        if value:
            setattr(elements, name, value)
    db.commit()
    return elements


def delete_from_db(
        db: Session,
        model: str,
        params: dict
    ):
    db.query(getattr(models, model)).filter(*(getattr(getattr(models, model), key) == value for key, value in params.items() if value)).delete()
    db.commit()
    return {'event': 'deleted'}

# session part
# def create_session(
#         db: Session,
#         user_id: int,
#         room_id: int
#     ):
#     new_db_session = ModelSession(user_id = user_id, room_id = room_id)
#     db.add(new_db_session)
#     db.commit()
#     return new_db_session

# def read_session(
#         db: Session,
#         params: dict,
#         is_first: bool
#     ):
#     if not any(value for value in params.values()):
#         users = db.query(ModelSession).all()
#     else:
#         users = db.query(ModelSession).filter(*(getattr(ModelSession, key) == value for key, value in params.items() if value)).all()

#     if not users:
#         return None
#     return users[0] if is_first else users

# def update_user(
#         db: Session,
#         params: dict,
#         params_to_change: dict
#     ):
#     user_in_db = db.query(ModelUser).filter(*(getattr(ModelUser, key) == value for key, value in params.items() if value)).first()
#     for name, value in params_to_change.items():
#         if value:
#             setattr(user_in_db, name, value)
#     db.commit()
#     return user_in_db

# def delete_user(
#         db: Session,
#         params: dict
#     ):
#     user_in_db = db.query(ModelUser).filter(*(getattr(ModelUser, key) == value for key, value in params.items() if value)).first()
#     db.delete(user_in_db)
#     db.commit()
#     return {'event': 'deleted'}


# def get_sessions_by_user(db: Session, user: UserSchema):
#     return db.query(ModelSession).filter(ModelSession.user_id == user.id).all()


# def get_sessions_by_room(db: Session, room: RoomSchema):
#     return db.query(ModelSession).filter(ModelSession.room_id == room.id).all()


# def get_session_by_room_and_user(db: Session, user_id: int, room_id: int):
#     return db.query(ModelSession).filter(ModelSession.user_id == user_id, ModelSession.room_id == room_id).first()


# def delete_session_crud(db: Session, user_id: int, room_id: int):
#     db_session = db.query(ModelSession).filter(ModelSession.user_id == user_id, ModelSession.room_id == room_id).first()
#     db.delete(db_session)
#     db.commit()
#     return get_session_by_room_and_user(db, user_id, room_id)




# # room part
# def get_all_rooms(db: Session):
#     return db.query(ModelRoom).all()


# def get_room_by_room_code(db: Session, room_code: str):
#     return db.query(ModelRoom).filter(ModelRoom.code == room_code).first()


# def create_room(db: Session, room: RoomSchema):
#     db_room = ModelRoom(room_id = room.room_id, code = room.code, app_id= room.app_id)
#     db.add(db_room)
#     db.commit()
#     return db_room


# # app part
# def create_app(db: Session, app: AppSchema):
#     db_app = ModelApp(access_key = app.access_key, secret = app.secret, management_key = app.management_key, template_id = app.template_id, date_status = app.date_status)
#     db.add(db_app)
#     db.commit()
#     return db_app


# def get_all_apps(db: Session):
#     return db.query(ModelApp).all()


# def get_app_by_access_key(db: Session, access_key: str):
#     return db.query(ModelApp).filter(ModelApp.access_key == access_key).first()


# def update_app_management_key(db: Session, app_id: int, management_key: str, date: str):
#     db_app = db.query(ModelApp).filter(ModelApp.id == app_id).first()
#     db_app.management_key = management_key
#     db_app.date_status = date
#     db.commit()
#     return management_key


# # game part
# def create_game(db: Session, room_id: int):
#     db_game = ModelGame(room_id = room_id)
#     db.add(db_game)
#     db.commit()
#     return db_game


# def get_game_by_id(db: Session, game_id: int):
#     return db.query(ModelGame).filter(ModelGame.id == game_id).first()


# def get_game_by_room_id_and_non_started(db: Session, room_id: int):
#     return db.query(ModelGame).filter(ModelGame.room_id == room_id, ModelGame.win == 0).first()


# def get_game_by_room_id_and_started(db: Session, room_id: int):
#     return db.query(ModelGame).filter(ModelGame.room_id == room_id, ModelGame.win == 2).first()


# def update_start_game(db: Session, game_id: int):
#     db_game = db.query(ModelGame).filter(ModelGame.id == game_id).first()
#     db_game.win = 2
#     db.commit()


# def get_games_by_room_id(db: Session, room_id: int, status: int=0):
#     return db.query(ModelGame).filter(ModelGame.room_id == room_id, ModelGame.win == status).all()


# def update_room(db: Session, game_id: int, elements_to_change: dict[str, int]):
#     db_game = db.query(ModelGame).filter(ModelGame.id == game_id).first()

#     if elements_to_change.get('evil_win') or elements_to_change.get('good_win'):
#         db_game.good_win += int(elements_to_change.get('good_win', 0))
#         db_game.evil_win += int(elements_to_change.get('evil_win', 0))
#         db_game.rejected_rounds = 0
#     else:
#         db_game.rejected_rounds += elements_to_change.get('rejected_rounds', 0)
    
#     db.commit()
#     return db_game


# def delete_game(db: Session, game_id: int):
#     db_game = db.query(ModelGame).filter(ModelGame.id == game_id).first()
#     db.delete(db_game)
#     db.commit()
#     return None


# def update_room_status(db: Session, game_id: int, win: int):
#     db_game = db.query(ModelGame).filter(ModelGame.id == game_id).first()
#     db_game.win = win
#     db.commit()
#     return db_game


# # active users part
# def create_active_user(db: Session, game_id: int, user_id: int):
#     db_game = db.query(ModelGame).filter(ModelGame.id == game_id).first()
#     db_active_user = db.query(ModelActiveUser).filter(ModelActiveUser.user_id == user_id, ModelActiveUser.game_id == game_id).first()
#     if not db_active_user:
#         db_active_user = ModelActiveUser(user_id = user_id, game_id = game_id, order = len(db_game.active_users))
#         db.add(db_active_user)
#         db.commit()


# def update_state(db: Session, game_id: int, user_id: int):
#     db_active_user = db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.user_id == user_id).first()
#     db_active_user.state = 0 if db_active_user.state else 1
#     db.commit()
#     db_states = db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.state == 1).all()
#     return len(db_states)


# def update_active_users(db: Session, game_id: int, users: dict[str, object]):
#     for value in users.values():
#         db_user = db.query(ModelUser).filter(ModelUser.email == value['name']).first()
#         db_active_user = db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.user_id == db_user.id).first()
#         db_active_user.role = value['role']
#         db_active_user.order = value['role']
#         db_active_user.mermaid = value['mermaid']
#     db.commit()


# def get_active_user(db: Session, game_id: int, user_id: int):
#     return db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.user_id == user_id).first()


# def get_active_users(db: Session, game_id: int):
#     return db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id).all()


# def update_active_user_mermaid(db: Session, game_id: int, user_id: int):
#     db_user = db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.mermaid == 1).first()
#     db_user.mermaid = 2
#     db_new_mermaid = db.query(ModelActiveUser).filter(ModelActiveUser.game_id == game_id, ModelActiveUser.user_id == user_id).first()
#     db_new_mermaid.mermaid = 1
#     db.commit()
#     return db_new_mermaid.role, db_user.email
