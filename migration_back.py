import asyncio

from sqlalchemy import text

from base import async_session_maker
from models.models import Users


async def get_user_old():
    async with async_session_maker() as session:
        users = await session.execute(text('select * from pupsik'))
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


async def put_user_new():
    async with async_session_maker() as session:
        users: list = await add_to_class_pups()

        for user in users:
            new_user = Users(
                telegram_id=user.tg_id,
                fullname=f'ИГОРЬ',
                username=user.tg_name
            )
            session.add(new_user)
        await session.commit()


asyncio.run(put_user_new())
