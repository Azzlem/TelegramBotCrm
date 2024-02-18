import asyncio
import json
import uuid

from sqlalchemy import select, exists

from base import async_session_maker
from order.models import User, Order


class Service:
    @staticmethod
    async def add_user(tg_username, tg_user_id):
        async with async_session_maker() as db_session:
            try:
                data = {
                    'tg_user_id': tg_user_id,
                    'name': tg_username
                }
                print(data)
                user = User(**data)
                print(user.tg_user_id)
                stmt = db_session.add(user)
                await db_session.commit()
                return tg_username
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
            user = await db_session.execute(select(User).where(User.tg_user_id == user_id))
            a = user.all()
            if not a:
                return False
            b = a[0][0].status
            if b == 1:
                return "user"
            if b == 2:
                return "admin"
            return False

    @staticmethod
    async def get_user(tg_user_id):
        async with async_session_maker() as db_session:
            user = await db_session.execute(select(User).filter(User.tg_user_id == tg_user_id))
            if user.all():
                return user
            return False

    @staticmethod
    async def add_order(data):
        async with async_session_maker() as db_session:
            date_add = {
                'user_id': int(data['user_id']),
                'client_name': data['client_name'],
                'client_phone': data['client_phone'],
                'device': data['device'],
                'mulfunction': data['mulfunction']

            }

            order = Order(**date_add)
            db_session.add(order)
            await db_session.commit()
            # print(order.id)
            # return order.id

    @staticmethod
    async def get_all_orders(user_id):
        async with async_session_maker() as db_session:
            orders = await db_session.execute(select(Order))
            return orders.all()

    @staticmethod
    async def list_order(user_id):
        data = await Service.get_all_orders(user_id)
        result = []
        for el in data:
            result.append(el[0])

        return result

    @staticmethod
    async def get_all_users():
        async with async_session_maker() as db_session:
            users = await db_session.execute(select(User))
            users = users.all()
            result = []
            for el in users:
                result.append(el[0])
            answer = ''
            for elem in result:
                answer += (f"Имя пользователя: {elem.name}\n"
                           f"ID в базе: {elem.id}\n"
                           f"Статус в компании: {elem.status}\n\n\n")

            return answer

# print(asyncio.run(Service().add_user({"id": "2", "tg_user_id": "555пкакуferwwfwатииаптfrf4reftмымвыамиавава5555", "name": "Alex", "phone": "89650005727"})))
# print(asyncio.run(Service.valid_user(3)))
# print(asyncio.run(Service.del_user(4)))
# print(asyncio.run(Service.get_user(2)))
