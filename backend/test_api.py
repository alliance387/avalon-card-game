from datetime import datetime

#models
from sql.models import ModelRoom

from webrtc import generateManagementToken
from util_func_api import get_info_users, edit_role_users

from sql.crud import get_room_by_100ms_room_id, update_app_management_key, delete_session_crud, get_all_users

def get_test_api_calls(app, db, URL_100MS):
    # util 
    def get_management_token(room: ModelRoom):
        if datetime.now().strftime('%Y-%m-%d') == room.app.date_status:
            return room.app.management_key
        else:
            new_management_token = generateManagementToken(room.app.access_key, room.app.secret)
            return update_app_management_key(db.session, room.app_id, new_management_token, datetime.now().strftime('%Y-%m-%d'))
        

    # test
    @app.post('/test/clear_room/{room_id}', tags=["test"])
    async def make_room_clear(room_id: str):
        room = get_room_by_100ms_room_id(db.session, room_id)
        HEADERS = {
            'Authorization': f'Bearer {get_management_token(room)}'
        }
        id_users = await get_info_users(url=f'{URL_100MS}active-rooms/{room_id}', headers=HEADERS)

        await edit_role_users(url=f'{URL_100MS}active-rooms/{room_id}', headers=HEADERS, id_users=id_users, is_test=True)

        return {'message': 'Ошибка'} if id_users == 'Произошла ошибка' else {"info_users": id_users}


    # test users
    @app.get('/test/get_all_users', tags=["test", "user"])
    async def get_all_users_for_test():
        return get_all_users(db.session)


    # test sessions
    @app.post('/test/delete_session', tags=["test", "session"])
    async def make_room_clear(room_id: int, user_id: int):
        return delete_session_crud(db.session, user_id, room_id)
    

    return [get_management_token,
            make_room_clear,
            get_all_users_for_test,
            make_room_clear]