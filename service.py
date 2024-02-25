from sqlalchemy import select, update
from order.models import User, Order
from base import async_session_maker
from service_base_actions import ServiceBaseActions


class Service:

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


    @staticmethod
    async def get_all_orders(user_id):
        async with async_session_maker() as db_session:
            orders = await db_session.execute(select(Order))
            return orders.all()

    @staticmethod
    async def get_all_orders_scalar() -> list:
        async with async_session_maker() as db_session:
            orders = await db_session.execute(select(Order))
            return orders.scalars().all()

    @staticmethod
    async def get_all_orders_user(data) -> list:
        async with async_session_maker() as db_session:
            print(data)
            user = await ServiceBaseActions.get_user(data.id)
            print(user)
            orders = await db_session.execute(select(Order).filter_by(user_id=user.id))
            return orders.scalars().all()

    @staticmethod
    async def list_order(user_id: int):
        data = await Service.get_all_orders(user_id)
        result = []
        for el in data:
            result.append(el[0])

        return result

    @staticmethod
    async def update_order(data):
        async with async_session_maker() as db_session:
            data_temp = data.pop('order_id')
            print(data_temp)
            await db_session.execute(update(Order).where(Order.id == int(data_temp)).values(
                user_id=int(data['user_id']),
                client_name=data['client_name'],
                client_phone=data['client_phone'],
                device=data['device'],
                mulfunction=data['mulfunction']
            ))
            await db_session.commit()
