"""Module of working with 100ms API updating users roles"""
from random import shuffle

import asyncio
from aiohttp import ClientSession


async def update_role_users(url: str,
                            headers: dict,
                            payload: dict,
                            id_user: str,
                            session: ClientSession):
    """
    Couroutine for changing role
    """
    async with session.post(url=f'{url}/peers/{id_user}', headers=headers, json=payload) as response:
        await response.json()


async def edit_role_users(url: str,
                          headers: dict,
                          id_users: dict,
                          is_test: bool = False):
    """
    Concurently change roles of peers in this room by isong 100ms API
    """
    roles = ['merlin', "percival", "mordred", "morgana"]
    shuffle(roles)
    keys_of_users = list(id_users.keys())
    shuffle(keys_of_users)
    if len(id_users) >= 7:
        roles.append('assasin')
    if len(id_users) >= 9:
        roles.append('oberon')

    data_for_tasks = []
    if not is_test:
        for role in roles:
            chosen_user_id = keys_of_users.pop()
            id_users[chosen_user_id]['role'] = role
            data_for_tasks.append((chosen_user_id, role))
    else:
        for chosen_user_id in keys_of_users:
            id_users[chosen_user_id]['role'] = 'guest'
            data_for_tasks.append((chosen_user_id, 'guest'))

    async with ClientSession() as session:
        tasks = [update_role_users(url, headers, {'role': role}, peer_id, session) 
                for peer_id, role in data_for_tasks]
        await asyncio.gather(*tasks)
        