from random import shuffle

# TODO 2: Имхо лучше наверное явно импортировать что нужно через from
import aiohttp
import asyncio
async def get_info_users(url: str, headers: dict) -> dict[str, dict[str, str]]:
# асинхронка хз робит ли
    # TODO: 1 лучше будет мне кажется ловить ошибки через response.status_code или явно вызывать ошибку через response.raise_for_status
    # https://requests.readthedocs.io/en/latest/user/quickstart/#response-status-codes
    arr_error = ['<Response [403]>', '<Response [404]>', '<Response [500]>']
    info_users = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url}/peers', headers=headers) as status:
            if str(status) in arr_error:
                return "Произошла ошибка"
            # TODO 3: Думаю лишние скобки(исправил)
            full_info_users = await status.json()
            id_users = list(full_info_users["peers"].keys())
            shuffle(id_users)
            for idx, id_user in enumerate(id_users):
                response_info_users = full_info_users["peers"][id_user]
                info_users[id_user] = {
                    'name': f'{response_info_users["name"]}',
                    'role': f'{response_info_users["role"]}',
                    'order': idx,  # for db
                    'mermaid': int(len(id_users) <= idx + 1) 
                }
            return info_users


# def get_info_users(url: str,
#                    headers: dict,):
#
#     arr_error = ['<Response [403]>', '<Response [404]>', '<Response [500]>']
#     info_users = {}
#     response = requests.request("GET", f'{url}/peers', headers=headers)
#     if str(response) in arr_error:
#         return "Произошла ошибка"
#
#     id_users = list(response.json()["peers"].keys())
#     shuffle(id_users)
#     for id_user in id_users:
#         response_info_users = (response.json()["peers"][id_user])
#         info_users[id_user] = {
#             'name':f'{response_info_users["name"]}',
#             'role':f'{response_info_users["role"]}'
#         }
#     return info_users