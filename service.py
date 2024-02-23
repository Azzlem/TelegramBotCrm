from sqlalchemy import select, update, delete
from order.models import User, Order
from base import async_session_maker


class Service:
    @staticmethod
    async def add_user(tg_username, tg_user_id):
        async with async_session_maker() as db_session:
            try:
                data = {
                    'tg_user_id': str(tg_user_id),
                    'name': tg_username
                }
                user = User(**data)
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
                await db_session.execute(delete(User).where(user.id == user_id))
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
    async def list_order(user_id: int):
        data = await Service.get_all_orders(user_id)
        result = []
        for el in data:
            result.append(el[0])

        return result

    @staticmethod
    async def get_all_users():
        async with async_session_maker() as db_session:
            users = await db_session.execute(select(User))
            users = users.scalars().all()
            return users
            # result = []
            # for el in users:
            #     result.append(el[0])
            # answer = ''
            # for elem in result:
            #     answer += (f"Имя пользователя: @{elem.name}\n"
            #                f"ID в базе: {elem.id}\n"
            #                f"Статус в компании: {elem.status}\n\n\n")
            #
            # return answer, len(result)

    @staticmethod
    async def change_perms_user(data):
        async with async_session_maker() as db_session:
            await db_session.execute(
                update(User).where(User.id == int(data['user_id'])).values(status=int(data['status'])))
            await db_session.commit()
            return True

    @staticmethod
    async def delete_user(res):
        async with async_session_maker() as db_session:
            await db_session.execute(delete(User).where(User.id == res['user_id']))
            await db_session.commit()
            return True

    @staticmethod
    async def update_order(data):
        async with async_session_maker() as db_session:
            data_temp = data.pop('id_order')
            print(data_temp)
            await db_session.execute(update(Order).where(Order.id == int(data_temp)).values(
                user_id=int(data['user_id']),
                client_name=data['client_name'],
                client_phone=data['client_phone'],
                device=data['device'],
                mulfunction=data['mulfunction']
            ))
            await db_session.commit()

