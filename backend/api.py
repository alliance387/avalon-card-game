from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def read_root():
    return { 
        'message': 'Hello bitch'
    }

@app.get('/user_order/{room_id}')
async def read_room_order(room_id: str):
    return { 
        'message': f'I dunno know what to do {room_id}'
    }
