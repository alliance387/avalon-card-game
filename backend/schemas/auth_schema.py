from pydantic import BaseModel, EmailStr


class User(BaseModel):
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

    class Config:
        schema_extra = {
            "example": {
                "email": "i_love_when_big@x.com",
                "password": "i_love_when_big"
            }
        }