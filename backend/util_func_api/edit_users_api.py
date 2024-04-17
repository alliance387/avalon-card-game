from random import shuffle

import requests


def update_role_users(url: str,
                      headers: dict,
                      payload: dict,
                      id_user: str):

    requests.request("POST", url=f'{url}/peers/{id_user}', headers=headers, json=payload)


def edit_role_users(url: str,
                    headers: dict,
                    id_users: list):

    copy_id_users = id_users.copy()
    shuffle(copy_id_users)
    roles = ['merlin', "percival", "mordred", "morgana"]
    shuffle(roles)
    if len(id_users) >= 5:
        if len(id_users) >= 7:
            roles.append('assasin')
        if len(id_users) >= 9:
            roles.append('oberon')
        for role in roles:
            payload = {
                'role': role
            }
            update_role_users(url=url, headers=headers, payload=payload, id_user=copy_id_users.pop())
    else:
        return print("Пользователей не достаточно")
