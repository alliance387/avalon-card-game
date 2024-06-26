from datetime import datetime
from typing import Optional

#models
from sql.models import ModelRoom

from webrtc import generateManagementToken
from util_func_api import get_info_users, edit_role_users

from sql.crud import create_element_in_db, read_from_db, update_from_db, delete_from_db
# from sql.crud import read_from_db, get_room_by_100ms_room_id, update_app_management_key, delete_session_crud, get_games_by_room_id, get_room_by_room_code, \
#                     delete_game

def get_test_api_calls(app, db, URL_100MS) -> list[callable]:
    # test
    @app.post('/test/clear_room/{room_id}', tags=['test'])
    async def make_room_clear(room_id: str):
        room = read_from_db(db.session, 'ModelRoom', {'room_id': room.room_id}, is_first=True)
        HEADERS = {
            'Authorization': f'Bearer {get_management_token(room)}'
        }
        id_users = await get_info_users(url=f'{URL_100MS}active-rooms/{room_id}', headers=HEADERS)

        await edit_role_users(url=f'{URL_100MS}active-rooms/{room_id}', headers=HEADERS, id_users=id_users, is_test=True)

        return {'message': 'Ошибка'} if id_users == 'Произошла ошибка' else {'info_users': id_users}


    # test users
    @app.get('/test/read_users', tags=['test-user'])
    async def read_crud_users(
            id: Optional[int] = 0, 
            full_name: Optional[str] = '', 
            email: Optional[str] = '', 
            password: Optional[str] = '', 
            is_first: Optional[bool] = False
        ):
        return read_from_db(db.session, 'ModelUser', {
            'id': id, 
            'full_name': full_name,
            'email': email,
            'password': password
        }, is_first)

    @app.get('/test/update_user', tags=['test-user'])
    async def update_crud_users(
            id: Optional[int] = 0, 
            full_name: Optional[str] = '', 
            email: Optional[str] = '', 
            password: Optional[str] = '', 
            id_to_change: Optional[int] = 0, 
            full_name_to_change: Optional[str] = '', 
            email_to_change: Optional[str] = '', 
            password_to_change: Optional[str] = ''
        ):
        return update_from_db(db.session, 'ModelUser', {
            'id': id, 
            'full_name': full_name,
            'email': email,
            'password': password
        }, {
            'id': id_to_change, 
            'full_name': full_name_to_change,
            'email': email_to_change,
            'password': password_to_change
        })
    
    @app.get('/test/delete_user', tags=['test-user'])
    async def delete_crud_user(
            id: Optional[int] = 0, 
            full_name: Optional[str] = '', 
            email: Optional[str] = '', 
            password: Optional[str] = ''
        ):
        return delete_from_db(db.session, 'ModelUser', {
            'id': id, 
            'full_name': full_name,
            'email': email,
            'password': password
        })

    # test sessions
    @app.post('/test/delete_session', tags=['test-session'])
    async def make_room_clear(room_id: int, user_id: int):
        return delete_from_db(db.session, 'ModelSession', {
            'room_id': room_id, 
            'user_id': user_id
        })


    # test games
    @app.get('/test/games_by_room', tags=['test-game'])
    async def show_all_games_by_room(room_key: str):
        actual_room_id = read_from_db(db.session, 'ModelRoom', {'code': room_key}, is_first=True).id
        return read_from_db(db.session, 'ModelGame', {'room_id': actual_room_id}, is_first=False)

    # test games
    @app.post('/test/delete_games_inactive', tags=['test-game'])
    async def delete_games_inactive(room_key: str, status: int):
        actual_room_id = read_from_db(db.session, 'ModelRoom', {'code': room_key}, is_first=True).id
        delete_from_db(db.session, 'ModelGame', {
            'room_id': actual_room_id, 
            'win': status
        })
        return {
            'message': 'all rooms inactive were deleted'
        }
    
    # test games
    @app.post('/test/delete_active_users', tags=['test-active-users'])
    async def delete_acitve_users(game_id: int):
        delete_from_db(db.session, 'ModelActiveUser', {
            'game_id': game_id
        })
        return {
            'message': 'all active users were deleted'
        }
    

    return [
            make_room_clear,
            read_crud_users,
            update_crud_users,
            delete_crud_user,
            make_room_clear,
            show_all_games_by_room,
            delete_games_inactive,
            delete_acitve_users
            ]

# util 
def get_management_token(room: ModelRoom, db: object) -> str:
    if datetime.now().strftime('%Y-%m-%d') == room.app.date_status:
        return room.app.management_key
    else:
        new_management_token = generateManagementToken(room.app.access_key, room.app.secret)
        update_from_db(db.session, 'ModelApp', {
            'id': room.app_id
        }, {
            'management_key': new_management_token, 
            'date_status': datetime.now().strftime('%Y-%m-%d')
        })
        return new_management_token