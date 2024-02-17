import asyncio
import json

from base import async_session_maker
from order.models import User


class Service:
    @staticmethod
    async def add_user(data, tg_user_id):
        async with async_session_maker() as db_session:
            try:
                data = json.loads(data)
                data['tg_user_id'] = str(tg_user_id)
                user = User(**data)
                print(user.tg_user_id)
                stmt = db_session.add(user)
                await db_session.commit()
            except:
                print("Ёпта")

    @staticmethod
    async def del_user(user_id):
        async with async_session_maker() as db_session:
            user = await db_session.get(User, user_id)
            if user is not None:
                await db_session.delete(user)
                await db_session.commit()
                return True
            return False

    @staticmethod
    async def valid_user(user_id):
        async with async_session_maker() as db_session:
            user = await db_session.get(User, user_id)
            if user is not None:
                return user.id == 2
            return False

    @staticmethod
    async def get_user(user_id):
        async with async_session_maker() as db_session:
            user = await db_session.get(User, user_id)
            if user is not None:
                return user
            return False

# print(asyncio.run(Service().add_user({"id": "2", "tg_user_id": "555пкакуferwwfwатииаптfrf4reftмымвыамиавава5555", "name": "Alex", "phone": "89650005727"})))
# print(asyncio.run(Service.valid_user(3)))
# print(asyncio.run(Service.del_user(4)))
# print(asyncio.run(Service.get_user(2)))
