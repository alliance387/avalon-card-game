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
from sql.crud import get_user_by_email, create_user, get_room_by_100ms_room_id, create_room, create_session, get_sessions_by_user, get_room_by_room_code, \
                    get_all_apps, create_app, get_app_by_access_key, get_all_rooms, get_game_by_id, update_room, update_room_status, get_game_by_room_id_and_non_started, \
                    get_active_user, update_active_user_mermaid, create_game, update_active_users, get_active_users, get_session_by_room_and_user, get_game_by_room_id_and_started, \
                    create_active_user, update_state, update_start_game
# utils
from auth import JWTBearer, signJWT
from util_func_api import get_info_users, edit_role_users
from test_api import get_test_api_calls, get_management_token

load_dotenv('.env')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

origins = [
    "https://avalon-card-game.vercel.app",
    "https://avalon-card-game-egor.vercel.app",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

URL_100MS = 'https://api.100ms.live/v2/'

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get('/room', tags=["room"])
async def get_all_rooms_api():
    return get_all_rooms(db.session)
 
    
@app.post('/room', response_model=RoomSchema, tags=["room"])
async def make_room(room: RoomSchema):
    if not get_room_by_100ms_room_id(db.session, room.room_id):
        return create_room(db.session, room)
    else:
        raise HTTPException(status_code=409, detail="Room already exists")


@app.post("/user/signup", tags=["user"])
async def make_user(user: UserSchema):
    if not get_user_by_email(db.session, user.email):
        create_user(db.session, user, pwd_context.hash(user.password))
        return signJWT(user.email)
    else:
        raise HTTPException(status_code=409, detail="Account already exists")


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema):
    found_user = get_user_by_email(db.session, user.email)
    if not found_user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    is_password_correct = pwd_context.verify(user.password, found_user.password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect password")
    else:
        return signJWT(user.email)

@app.post("/session", dependencies=[Depends(JWTBearer())], tags=["session"])
async def make_session(room_code: str, user_email: str):
    found_user = get_user_by_email(db.session, user_email)
    if not found_user:
        return {
            'error': 'user not found'
        }
    found_room = get_room_by_room_code(db.session, room_code)
    if not found_room:
        return {
            'error': 'room not found'
        }
    if not get_session_by_room_and_user(db.session, found_user.id, found_room.id):
        return create_session(db.session, SessionSchema(room_id=found_room.id, user_id=found_user.id))
    else:
        return {
            'warning': 'session exists'
        }
    

@app.get("/session", dependencies=[Depends(JWTBearer())], tags=["session"])
async def get_sessions(user_email: str):
    sessions_by_user = get_sessions_by_user(db.session, get_user_by_email(db.session, user_email))
    return [session.rooms_in_session for session in sessions_by_user] 


@app.post("/apps", tags=["apps"])
async def make_app(app: AppSchema):
    found_app = get_app_by_access_key(db.session, app.access_key)
    if not found_app:
        return create_app(db.session, app)
    else:
        return {
            'error': 'app exists'
        }

@app.get("/apps", tags=["apps"])
async def get_apps():
    return get_all_apps(db.session)


# game logic
@app.post('/game/enter_room', tags=["games"])
async def enter_room_pass(room_code: str, user_email: str):
    found_room = get_room_by_room_code(db.session, room_code)
    found_user = get_user_by_email(db.session, user_email)
    
    if any(game.win == 2 for game in found_room.games):
        if any(lobby.game.room_id == found_room.id for lobby in found_user.active_in_lobbies):
            return {
                'event': 'reenter',
                'game_id': game.id
            }   
        else:
            return {
                'error': 'match is going on'
            }
    else:
        if all(game.win != 0 for game in found_room.games):
            game = create_game(db.session, found_room.id)
        else:
            # TODO: BETTER got without db
            game = get_game_by_room_id_and_non_started(db.session, found_room.id)

        create_active_user(db.session, game.id, found_user.id)

        return {
            'event': 'enter',
            'game_id': game.id
        }




@app.get('/game/game-info', tags=["games"])
async def get_game(game_id: int):
    game = get_game_by_id(db.session, game_id)
    return {
        'active_users': get_active_users(db.session, game.id),
        'game': game
    }

@app.post('/game/change_state', tags=["games"])
async def change_state(game_id: int, user_email: str):
    found_user = get_user_by_email(db.session, user_email)
    count_states = update_state(db.session, game_id, found_user.id)
    game = get_game_by_id(db.session, game_id)

    # Start game
    if game.win == 0 and count_states >= 5:
        update_start_game(db.session, game.id)

        HEADERS = {
            'Authorization': f'Bearer {get_management_token(game.room.room_id, db)}'
        }
        id_users = await get_info_users(url=f'{URL_100MS}active-rooms/{game.room.room_id}', headers=HEADERS)

        await edit_role_users(url=f'{URL_100MS}active-rooms/{game.room.room_id}', headers=HEADERS, id_users=id_users)
        update_active_users(db.session, game.id, id_users)

    return {
        'event': 'changed'
    }


@app.get('/game/info-users', tags=["games"])
async def read_info_users(room_id: str):
    room = get_room_by_100ms_room_id(db.session, room_id)
    HEADERS = {
        'Authorization': f'Bearer {get_management_token(room, db)}'
    }
    info_users = await get_info_users(url=f'{URL_100MS}active-rooms/{room_id}', headers=HEADERS)
    return {'message': 'Ошибка'} if info_users == 'Произошла ошибка' else {"info_users": info_users}


@app.post("/game/poll", tags=["games"])
async def count_poll(game_id: int, accept_quest: int) -> dict[str, int]:
    game = get_game_by_id(db.session, game_id)
    if accept_quest * 2 > game.number:
        return {
            'is_quest_accepted': 1,
            'rejected_rounds': 0
        }
    else:
        game = update_room(db.session, game.id, {'rejected_rounds': 1})
        if game.rejected_rounds >= 5:
            update_room_status(db.session, game.id, -1)
            return {
                'win': 'evil'
            }
        else: 
            {
                'is_quest_accepted': 0,
                'rejected_rounds': 1
            }


@app.post("/game/quest", tags=["games"])
async def make_quest(game_id: int, is_success: bool, fails: int) -> dict[str, str]:
    game = update_room(db.session, game_id, {'good_win': int(is_success), 'evil_win': int(not is_success)})
    if game.evil_win < 3 and game.good_win < 3:
        return {
            'fails': fails,
            'is_quest_accepted': 0,
            'good_win': game.good_win,
            'evil_win': game.evil_win,
            'rejected_rounds': 0
        }
    else:
        if game.evil_win >= 3:
            update_room_status(db.session, game.id, -1)
            return {
                'win': 'evil'
            }
        else:
            return {
                'event': 'assasin',
                'fails': fails,
                'is_quest_accepted': 0,
                'good_win': game.good_win,
                'evil_win': game.evil_win,
                'rejected_rounds': 0
            }


@app.post("/game/assasin_move", tags=["games"])
async def assasin_move(game_id: int, email: str) -> dict[str, str]:
    suspected_merlin = get_user_by_email(db.session, email)
    active_user_info = get_active_user(db.session, game_id, suspected_merlin.id)
    if active_user_info.role == 'merlin':
        update_room_status(db.session, game_id, -1)
        return {
            'win': 'evil'
        }
    else:
        update_room_status(db.session, game_id, 1)
        return {
            'win': 'good'
        }
    

@app.post("/game/mermaid_move", tags=["games"])
async def mermaid_move(game_id: int, email: str) -> dict[str, str]:
    new_mermaid = get_user_by_email(db.session, email)
    active_user_info = get_active_user(db.session, game_id, new_mermaid.id)
    if active_user_info.mermaid > 0:
        return {
            'warning': 'you can not change this person to mermaid'
        }
    else:
        new_mermaid_role, last_mermaid_email = update_active_user_mermaid(db.session, game_id, new_mermaid.id)
        return {
            'role': new_mermaid_role,
            'last_mermaid': last_mermaid_email
        }

get_test_api_calls(app, db, URL_100MS)

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
