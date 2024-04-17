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
    roles = ['merlin', "percival", "mordred", "morgana"]
    shuffle(roles)
    keys_of_users = iter(shuffle(id_users.keys()))
    if len(id_users) >= 5:
        if len(id_users) >= 7:
            roles.append('assasin')
        if len(id_users) >= 9:
            roles.append('oberon')
        for role in roles:
            payload = {
                'role': role
            }
            # for db
            chosen_user_id = next(keys_of_users)
            id_users[chosen_user_id]['role'] = role
            # TODO: Думаю лучше будет это засунуть в асинхронку чтобы не ждать пока 5-10 ролей будем добавлять
            update_role_users(url=url, headers=headers, payload=payload, id_user=chosen_user_id)
        
    else:
        # TODO: Имхо кажется лучше будет лучше убрать либо отправить ошибку
        return print("Пользователей не достаточно")
