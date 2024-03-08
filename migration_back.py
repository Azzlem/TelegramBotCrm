import asyncio
import json

from base import async_session_maker
from models.models import Users


async def get():
    with open("data2.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        return data


async def put_user_new():
    async with async_session_maker() as session:
        users: list = await get()
        for user in users:
            new_user = Users(
                telegram_id=user["tg_id"],
                fullname=f'ИГОРЬ',
                username=user["tg_name"]
            )
            session.add(new_user)
        await session.commit()


asyncio.run(put_user_new())
