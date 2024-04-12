from pydantic import BaseModel


class Room(BaseModel):
    room_id:str
    code:str

    class Config:
        orm_mode = True
