from fastapi import FastAPI
import uvicorn

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


if __name__ == "__main__":
   uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)