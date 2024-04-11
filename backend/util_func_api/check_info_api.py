from random import shuffle

import requests


def get_info_users(url: str,
                   headers,
                   response_info_users=None):
    error = ['<Response [403]>', '<Response [404]>', '<Response [500]>']
    info_users = {}
    response = requests.request("GET", f'{url}/peers', headers=headers)

    if str(response) in error:
        return "Произошла ошибка"

    id_users = list(response.json()["peers"].keys())
    shuffle(id_users)
    for id_user in id_users:
        response_info_users = (response.json()["peers"][id_user])
        info_users[id_user] = {
            'name':f'{response_info_users["name"]}',
            'role':f'{response_info_users["role"]}'
        }
    return info_users