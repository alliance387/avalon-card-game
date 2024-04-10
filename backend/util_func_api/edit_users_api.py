import random
import requests

def edit_role_users(url: str,
                    headers,
                    id_users: list):

    copy_id_users = id_users.copy()
    random.shuffle(copy_id_users)
    roles = ['guest',"guest"]
    random.shuffle(roles)
    if len(id_users) >= 3:
        for role in roles:
            payload = {
                'role': role
            }
            requests.post(url= f'{url}/{copy_id_users.pop()}', headers=headers, json=payload)

    # roles = ['Merlin', "Percival", "Mordred", "Morgana"]
    # random.shuffle(roles)
    # if len(id_users) >= 5:
    #     for role in roles:
    #         payload = {
    #             'roles': i
    #         }
    #         requests.post(url= f'{url}/{copy_id_users.pop()}', headers=headers, json=payload)
    # if len(id_users) >= 7:
    #     payload = {'role': 'Assasin'}
    #     requests.post(url= f'{url}/{copy_id_users.pop()}', headers=headers, json=payload)
    # if len(id_users) >= 9:
    #     payload = {'role': 'Oberon'}
    #     requests.post(url= f'{url}/{copy_id_users.pop()}', headers=headers, json=payload)

    else:
        return print("Пользователей не достаточно")
