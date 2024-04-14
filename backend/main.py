import os
from datetime import datetime

from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

#schemas
from sql.schema import UserSchema, UserLoginSchema, RoomSchema, SessionSchema, AppSchema
#models
from sql.models import ModelRoom
# crud
from sql.crud import get_user_by_email, create_user, get_room_by_100ms_room_id, create_room, create_session, get_sessions_by_user, get_room_by_room_code, \
                    get_all_apps, create_app, get_app_by_access_key, get_all_rooms, update_app_management_key
# utils
from auth import JWTBearer, signJWT
from webrtc import generateManagementToken

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

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get('/room/', tags=["room"])
async def get_all_rooms_api():
    return get_all_rooms(db.session)
 
    
@app.post('/room/', response_model=RoomSchema, tags=["room"])
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
    if found_user:
        found_room = get_room_by_room_code(db.session, room_code)
        if found_room:
            return create_session(db.session, SessionSchema(room_id=found_room.id, user_id=found_user.id))
        else:
            return {
                'warning': 'Session by this user exists'
            }
    else:
        return {
            'error': 'user not found'
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


# util 
def get_management_token(room: ModelRoom):
    if datetime.now().strftime('%Y-%m-%d') == room.app.date_status:
        return room.app.management_key
    else:
        new_management_token = generateManagementToken(room.app.access_key, room.app.secret)
        return update_app_management_key(db.session, room.app_id, new_management_token, datetime.now().strftime('%Y-%m-%d'))

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
