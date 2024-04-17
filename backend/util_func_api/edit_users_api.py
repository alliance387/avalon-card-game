from random import shuffle

import requests
import asyncio
import aiohttp

async def update_role_users(url: str,
                      headers: dict,
                      payload: dict,
                      id_user: str):

    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{url}/peers/{id_user}', headers=headers, json=payload) as response:
            print(f"Status: {response.status}")
            print(await response.json())


async def edit_role_users(url: str,
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
            # TODO: Думаю лучше будет это засунуть в асинхронку чтобы не ждать пока 5-10 ролей будем добавлять(закинул)
            task_update_role = asyncio.create_task(update_role_users(url=url, headers=headers, payload=payload, id_user=chosen_user_id))
            await task_update_role

        
    # else:
        # TODO: Имхо кажется лучше будет лучше убрать либо отправить ошибку(ну да по идеи фронт может блочитб или давать команды)
        # return print("Пользователей не достаточно")
