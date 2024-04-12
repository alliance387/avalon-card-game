import os

from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from passlib.context import CryptContext

#schemas
from schemas import UserSchema, UserLoginSchema, RoomSchema
# models
from models import Room as ModelRoom, User as ModelUser
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


@app.post('/room/', response_model=RoomSchema)
async def room(room: RoomSchema):
    db_room = ModelRoom(room_id=room.room_id, code=room.code)
    db.session.add(db_room)
    db.session.commit()
    return db_room


@app.get('/room/')
async def room():
    room = db.session.query(ModelRoom).all()
    return room


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema):
    if db.session.query(ModelUser).filter_by(email=user.email).count() < 1:
        hashed_password = pwd_context.hash(user.password)
        user = ModelUser(full_name = user.full_name, email = user.email, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        return signJWT(user.email)
    else:
        raise HTTPException(status_code=409, detail="Account already exists")


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema):
    found_user = db.session.query(ModelUser).filter(ModelUser.email == user.email).first()
    if not found_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    is_password_correct = pwd_context.verify(user.password, found_user.password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    else:
        return signJWT(user.email)


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
