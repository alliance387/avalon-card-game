import os

from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from passlib.context import CryptContext

#schemas
from sql.schema import UserSchema, UserLoginSchema, RoomSchema, SessionSchema
# models
from sql.models import ModelRoom
# crud
from sql.crud import get_user_by_email, create_user, get_room_by_100ms_room_id, create_room, create_session, get_sessions_by_user
# utils
from auth import JWTBearer, signJWT

load_dotenv('.env')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.get("/")
async def root():
    return {"message": "hello world"}


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
async def make_session(ms100_room_id: str, user_email: str):
    found_user = get_user_by_email(db.session, user_email)
    if found_user:
        found_room = get_room_by_100ms_room_id(db.session, ms100_room_id)
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


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
