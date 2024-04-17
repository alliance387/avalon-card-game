from random import shuffle

import requests
import aiohttp
import asyncio

async def get_info_users(url: str,
                   headers: dict,):
# асинхронка хз робит ли
    arr_error = ['<Response [403]>', '<Response [404]>', '<Response [500]>']
    info_users = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url}/peers', headers=headers) as status:
            if str(status) in arr_error:
                return "Произошла ошибка"
            full_info_users = (await status.json())
            id_users = list(full_info_users["peers"].keys())
            shuffle(id_users)
            for id_user in id_users:
                response_info_users = full_info_users["peers"][id_user]
                info_users[id_user] = {
                    'name': f'{response_info_users["name"]}',
                    'role': f'{response_info_users["role"]}'
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