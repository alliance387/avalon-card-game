import os

from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import asyncio

#schemas
from sql.schema import UserSchema, UserLoginSchema, RoomSchema, SessionSchema, AppSchema
# crud
from sql.crud import create_element_in_db, read_from_db, update_from_db, delete_from_db
# from sql.crud import get_room_by_100ms_room_id, create_room, create_session, get_sessions_by_user, get_room_by_room_code, \
#                     get_all_apps, create_app, get_app_by_access_key, get_all_rooms, get_game_by_id, update_room, update_room_status, get_game_by_room_id_and_non_started, \
#                     get_active_user, update_active_user_mermaid, create_game, update_active_users, get_active_users, get_session_by_room_and_user, get_game_by_room_id_and_started, \
#                     create_active_user, update_state, update_start_game
# utils
from auth import JWTBearer, signJWT
from util_func_api import get_info_users, edit_role_users
from test_api import get_test_api_calls, get_management_token

load_dotenv('.env')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

origins = [
    'https://avalon-card-game.vercel.app',
    'https://avalon-card-game-egor.vercel.app',
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

URL_100MS = 'https://api.100ms.live/v2/'

@app.get('/')
async def root():
    return {'message': 'hello world'}


@app.get('/room', tags=['room'])
async def get_all_rooms_api():
    return read_from_db(db.session, 'ModelRoom', {}, is_first=False)
 
    
@app.post('/room', response_model=RoomSchema, tags=['room'])
async def make_room(room: RoomSchema):
    if not read_from_db(db.session, 'ModelRoom', {'room_id': room.room_id}, is_first=True):
        return create_element_in_db(db.session, 'Modeluser', {
            'room_id': room.room_id, 
            'code': room.code
        })
    else:
        raise HTTPException(status_code=409, detail='Room already exists')


@app.post('/user/signup', tags=['user'])
async def make_user(user: UserSchema):
    if not read_from_db(db.session, 'ModelUser', {'email': user.email}, is_first=True):
        create_element_in_db(db.session, 'Modeluser', {
            'full_name': user.full_name, 
            'email': user.email, 
            'password': pwd_context.hash(user.password)
        })
        return signJWT(user.email)
    else:
        raise HTTPException(status_code=409, detail='Account already exists')


@app.post('/user/login', tags=['user'])
async def user_login(user: UserLoginSchema):
    found_user = read_from_db(db.session, 'ModelUser', {'email': user.email}, is_first=True)
    if not found_user:
        raise HTTPException(status_code=400, detail='Incorrect username')
    
    is_password_correct = pwd_context.verify(user.password, found_user.password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail='Incorrect password')
    else:
        return signJWT(user.email)

@app.post('/session', dependencies=[Depends(JWTBearer())], tags=['session'])
async def make_session(room_code: str, user_email: str):
    found_user = read_from_db(db.session, 'ModelUser', {'email': user_email}, is_first=True)
    if not found_user:
        return {
            'error': 'user not found'
        }
    found_room = read_from_db(db.session, 'ModelRoom', {'code': room_code}, is_first=True)
    if not found_room:
        return {
            'error': 'room not found'
        }
    
    if not read_from_db(db.session, 'ModelSession', {'user_id': found_user.id, 'room_id': found_room.id}, is_first=True):
        return create_element_in_db(db.session, 'ModelSession', {
            'user_id': found_user.id, 
            'room_id': found_room.id
        })
    else:
        return {
            'warning': 'session exists'
        }
    

@app.get('/session', dependencies=[Depends(JWTBearer())], tags=['session'])
async def get_sessions(user_email: str):
    sessions_by_user = read_from_db(db.session, 'ModelSession', {
        'user_id': read_from_db(db.session, 'ModelUser', {'email': user_email}, is_first=True).id
    }, is_first=False)
    return [session.rooms_in_session for session in sessions_by_user] 


@app.post('/apps', tags=['apps'])
async def make_app(app: AppSchema):
    found_app = read_from_db(db.session, 'ModelApp', {
        'access_key': app.access_key
    }, is_first=True)
    if not found_app:
        return create_element_in_db(db.session, 'ModelApp', {
            'access_key': app.access_key, 
            'secret': app.secret, 
            'management_key': app.management_key, 
            'template_id': app.template_id, 
            'date_status': app.date_status
        })
    else:
        return {
            'error': 'app exists'
        }

@app.get('/apps', tags=['apps'])
async def get_apps():
    return read_from_db(db.session, 'ModelApp', {}, is_first=False)


# game logic
@app.post('/game/enter_room', tags=['games'])
async def enter_room_pass(room_code: str, user_email: str):
    found_room = read_from_db(db.session, 'ModelRoom', {'code': room_code}, is_first=True)
    found_user = read_from_db(db.session, 'ModelUser', {'email': user_email}, is_first=True)
    
    if any(game.win == 2 for game in found_room.games):
        if any(lobby.game and lobby.game.room_id == found_room.id for lobby in found_user.active_in_lobbies):
            return {
                'event': 'reenter',
                'game_id': read_from_db(db.session, 'ModelGame', {'room_id': found_room.id, 'win': 2}, is_first=True).id
            }   
        else:
            return {
                'error': 'match is going on'
            }
    else:
        if all(game.win != 0 for game in found_room.games):
            game = create_element_in_db(db.session, 'ModelGame', {
                'room_id':found_room.id
            })
        else:
            game = read_from_db(db.session, 'ModelGame', {'room_id': found_room.id, 'win': 0}, is_first=True)

        create_element_in_db(db.session, 'ModelActiveUser', {
            'game_id': game.id, 
            'user_id': found_user.id, 
            'order': len(read_from_db(db.session, 'ModelActiveUser', {'game_id': game.id}, is_first=False)),
        })
        return {
            'event': 'enter',
            'game_id': game.id
        }




@app.get('/game/game-info', tags=['games'])
async def get_game(game_id: int):
    game = read_from_db(db.session, 'ModelGame', {'id': game_id}, is_first=True)
    return {
        'active_users': {
            active_user.user.email: 
            {
                'user_id': active_user.user_id,
                'order': active_user.order,
                'state': active_user.state,
                'armed': active_user.armed,
                'mermaid': active_user.mermaid,
                'mission': active_user.mission,
                'is_leader': active_user.is_leader,
            } for active_user in read_from_db(db.session, 'ModelActiveUser', {'game_id': game_id}, is_first=False)
            },
        'game': game
    }

@app.post('/game/change_state', tags=['games'])
async def change_state(game_id: int, user_email: str):
    found_user = read_from_db(db.session, 'ModelUser', {'email': user_email}, is_first=True)
    for lobby in found_user.active_in_lobbies:
        if lobby.game_id == game_id:
            current_state = lobby.state
            break
    current_state = 0 if current_state else 1
    current_state = update_from_db(db.session, 'ModelActiveUser', {'game_id': game_id, 'user_id': found_user.id}, {'state': current_state})

    game = read_from_db(db.session, 'ModelGame', {'id': game_id}, is_first=True)

    # Start game
    if game.win == 0 and len(active_user.state for active_user in game.active_users) >= 5:
        update_from_db(db.session, 'ModelGame', {'game_id': game_id}, {'win': 2})

        HEADERS = {
            'Authorization': f'Bearer {get_management_token(game.room.room_id, db)}'
        }
        id_users = await get_info_users(url=f'{URL_100MS}active-rooms/{game.room.room_id}', headers=HEADERS)

        await edit_role_users(url=f'{URL_100MS}active-rooms/{game.room.room_id}', headers=HEADERS, id_users=id_users)
        for user in id_users:
            user_id = read_from_db(db.session, 'ModelUser', {'email': user['name']}, is_first=True).id
            update_from_db(db.session, 'ModelActiveUser', {'game_id': game_id, 'user_id': user_id}, {
                'role': user['role'],
                'order': user['order'],
                'mermaid': 1 if user['order'] == len(id_users) - 1 else 0,
                'is_leader': 1 if user['order'] == 0 else 0
            })

    return {
        'event': 'changed'
    }


@app.get('/game/info-users', tags=['games'])
async def read_info_users(room_id: str):
    room = read_from_db(db.session, 'ModelRoom', {'room_id': room_id}, is_first=True)
    HEADERS = {
        'Authorization': f'Bearer {get_management_token(room, db)}'
    }
    info_users = await get_info_users(url=f'{URL_100MS}active-rooms/{room_id}', headers=HEADERS)
    return {'message': 'Ошибка'} if info_users == 'Произошла ошибка' else {'info_users': info_users}


# @app.post('/game/poll', tags=['games'])
# async def count_poll(game_id: int, accept_quest: int) -> dict[str, int]:
#     game = get_game_by_id(db.session, game_id)
#     if accept_quest * 2 > game.number:
#         return {
#             'is_quest_accepted': 1,
#             'rejected_rounds': 0
#         }
#     else:
#         game = update_room(db.session, game.id, {'rejected_rounds': 1})
#         if game.rejected_rounds >= 5:
#             update_room_status(db.session, game.id, -1)
#             return {
#                 'win': 'evil'
#             }
#         else: 
#             {
#                 'is_quest_accepted': 0,
#                 'rejected_rounds': 1
#             }


# @app.post('/game/quest', tags=['games'])
# async def make_quest(game_id: int, is_success: bool, fails: int) -> dict[str, str]:
#     game = update_room(db.session, game_id, {'good_win': int(is_success), 'evil_win': int(not is_success)})
#     if game.evil_win < 3 and game.good_win < 3:
#         return {
#             'fails': fails,
#             'is_quest_accepted': 0,
#             'good_win': game.good_win,
#             'evil_win': game.evil_win,
#             'rejected_rounds': 0
#         }
#     else:
#         if game.evil_win >= 3:
#             update_room_status(db.session, game.id, -1)
#             return {
#                 'win': 'evil'
#             }
#         else:
#             return {
#                 'event': 'assasin',
#                 'fails': fails,
#                 'is_quest_accepted': 0,
#                 'good_win': game.good_win,
#                 'evil_win': game.evil_win,
#                 'rejected_rounds': 0
#             }


# @app.post('/game/assasin_move', tags=['games'])
# async def assasin_move(game_id: int, email: str) -> dict[str, str]:
#     suspected_merlin = read_from_db(db.session, 'ModelUser', {'email': email}, is_first=True)
#     active_user_info = get_active_user(db.session, game_id, suspected_merlin.id)
#     if active_user_info.role == 'merlin':
#         update_room_status(db.session, game_id, -1)
#         return {
#             'win': 'evil'
#         }
#     else:
#         update_room_status(db.session, game_id, 1)
#         return {
#             'win': 'good'
#         }
    

# @app.post('/game/mermaid_move', tags=['games'])
# async def mermaid_move(game_id: int, email: str) -> dict[str, str]:
#     new_mermaid = read_from_db(db.session, 'ModelUser', {'email': email}, is_first=True)
#     active_user_info = get_active_user(db.session, game_id, new_mermaid.id)
#     if active_user_info.mermaid > 0:
#         return {
#             'warning': 'you can not change this person to mermaid'
#         }
#     else:
#         new_mermaid_role, last_mermaid_email = update_active_user_mermaid(db.session, game_id, new_mermaid.id)
#         return {
#             'role': new_mermaid_role,
#             'last_mermaid': last_mermaid_email
#         }

get_test_api_calls(app, db, URL_100MS)

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
