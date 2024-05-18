from pydantic import BaseModel, EmailStr

# room part

class RoomSchema(BaseModel):
    room_id:str
    code:str
    app_id:int

    class Config:
        orm_mode = True


# user part

class UserSchema(BaseModel):
    full_name: str 
    email: EmailStr 
    password: str

    class Config:
        schema_extra = {
            "example": {
                "full_name": "Lovin Inside You",
                "email": "i_love_when_big@x.com",
                "password": "i_love_when_big"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str 

    class Config:
        schema_extra = {
            "example": {
                "email": "i_love_when_big@x.com",
                "password": "i_love_when_big"
            }
        }

# session

class SessionSchema(BaseModel):
    user_id: int
    room_id: int

    class Config:
        orm_mode = True


# app
class AppSchema(BaseModel):
    access_key: str
    secret: str
    management_key: str
    template_id: str
    date_status: str

    class Config:
        orm_mode = True


# game
class GameSchema(BaseModel):
    good_win: int
    evil_win: int
    rejected_rounds: int

    class Config:
        orm_mode = True


class ActiveUserSchema(BaseModel):
    role: int
    user_id: int
    game_id: int

    class Config:
        orm_mode = True