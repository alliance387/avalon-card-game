import os

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from util_func_api import  get_info_users

app = FastAPI()
load_dotenv()
TOKEN_100MC = os.environ.get('TOKEN_100MC')
URL = 'https://api.100ms.live/v2/'
HEADERS = {
    'Authorization': TOKEN_100MC
}


@app.get('/')
async def read_root():
    return { 
        'message': 'Hello bitch'
    }


@app.get('/user_order/{room_id}')
async def start_game(room_id: str):
    id_users = get_info_users(url=f'{URL}active-rooms/{room_id}', headers=HEADERS)
    return {'message':'Ошибка'} if id_users =='Произошла ошибка' else {"info_users": list(id_users.keys())}


@app.get('/info_users/{room_id}')
async def read_info_users(room_id: str):
    info_users = get_info_users(url=f'{URL}active-rooms/{room_id}',headers=HEADERS)
    return {'message':'Ошибка'} if info_users =='Произошла ошибка' else {"info_users": info_users}




if __name__ == "__main__":
   uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)