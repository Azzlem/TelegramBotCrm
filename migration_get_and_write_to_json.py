import asyncio
import json
from sqlalchemy import text
from base import async_session_maker


async def get_user_old():
    async with async_session_maker() as session:
        users = await session.execute(text('select * from public.user'))
        users = users.all()
        return users


class Pups:
    pups = []

    def __init__(self, data):
        self.id = data[0]
        self.tg_id = data[1]
        self.tg_name = data[2]
        self.role = data[3]

    def __str__(self):
        return f'{self.tg_id} {self.tg_name} {self.role}'


async def add_to_class_pups():
    users = await get_user_old()
    for user in users:
        Pups.pups.append(Pups(user))

    return Pups.pups


async def write_file_database():
    with open('data2.json', 'a') as f:
        users = await add_to_class_pups()
        users_new = []
        for el in users:
            users_new.append(el.__dict__)
        json.dump(users_new, f)


asyncio.run(write_file_database())
