import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Room as SchemaRoom

from models import Room as ModelRoom

import os
from dotenv import load_dotenv

load_dotenv('.env')


app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/room/', response_model=SchemaRoom)
async def room(room: SchemaRoom):
    db_room = ModelRoom(room_id=room.room_id, code=room.code)
    db.session.add(db_room)
    db.session.commit()
    return db_room


@app.get('/room/')
async def room():
    book = db.session.query(ModelRoom).all()
    return book


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)