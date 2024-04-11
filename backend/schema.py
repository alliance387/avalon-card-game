from pydantic import BaseModel


class Room(BaseModel):
    room_id:str
    code:int

    class Config:
        orm_mode = True