import asyncio
import json

from base import async_session_maker


async def get():
    with open("data2.json", "r") as f:
        data = json.load(f)
        return data


async def put_user_new():
    async with async_session_maker() as session:
        users: list = await get()
        print(users[0])
        # for user in users:
        #     new_user = Users(
        #         telegram_id=user.tg_id,
        #         fullname=f'ИГОРЬ',
        #         username=user.tg_name
        #     )
        #     session.add(new_user)
        # await session.commit()


asyncio.run(put_user_new())
