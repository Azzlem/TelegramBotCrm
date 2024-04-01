from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from base import async_session_maker
from models.models import Orders, Users
from permission import is_owner_admin


class OrdersActions:
    model = Orders

    @classmethod
    async def add_orders(cls, data):
        async with async_session_maker() as session:
            order = Orders(**data)
            session.add(order)
            await session.commit()

    @classmethod
    async def create_orders(cls, customer_id, user_id):
        async with async_session_maker() as session:
            order = Orders(customer_id=customer_id, user_id=user_id)
            session.add(order)
            await session.commit()
            return order

    @classmethod
    async def create_orders_without_user(cls, customer_id):
        async with async_session_maker() as session:
            order = Orders(customer_id=customer_id)
            session.add(order)
            await session.commit()
            return order

    @classmethod
    async def get_orders(cls, data):
        async with async_session_maker() as db:
            orders = await db.execute(select(Orders).where(Orders.user_id == data.id))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_orders_with_customer(cls, data):
        async with async_session_maker() as db:
            orders = await db.execute(select(Orders).where(
                Orders.user_id == data.id
            ).options(selectinload(cls.model.customer)))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_all_orders(cls):
        async with async_session_maker() as db:
            orders = await db.execute(select(Orders))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_all_orders_with_customer(cls):
        async with async_session_maker() as db:
            orders = await db.execute(select(Orders).options(selectinload(cls.model.customer)))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_all_orders_with_all_info(cls):
        async with async_session_maker() as db:
            orders = await db.execute(select(Orders).
                                      options(selectinload(cls.model.customer)).
                                      options(selectinload(cls.model.user)).
                                      options(selectinload(cls.model.items)).
                                      options(selectinload(cls.model.components)))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_all_orders_with_all_info_for_id(cls, data):
        async with async_session_maker() as db:
            user = await db.execute(select(Users).filter_by(telegram_id=data.id))
            user = user.scalars().first()
            orders = await db.execute(select(Orders).filter_by(user_id=user.id).
                                      options(selectinload(cls.model.customer)).
                                      options(selectinload(cls.model.user)).
                                      options(selectinload(cls.model.items)).
                                      options(selectinload(cls.model.components)))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_all_orders_accepted(cls, user, status):
        async with async_session_maker() as db:
            print(user.username)
            if is_owner_admin(user):
                orders = await db.execute(select(Orders).filter_by(status=status).
                                          options(selectinload(cls.model.customer)).
                                          options(selectinload(cls.model.items)))
            elif user:
                orders = await db.execute(select(Orders).filter_by(user_id=user.id).filter_by(status=status).
                                          options(selectinload(cls.model.customer)).
                                          options(selectinload(cls.model.items)))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def appoint_user_to_order(cls, user_id, order_id):
        async with async_session_maker() as db:
            if not user_id:
                return False
            else:
                await db.execute(update(Orders).where(Orders.id == order_id).values(user_id=user_id))
                await db.commit()
                return True

    @classmethod
    async def get_order(cls, order_id):
        async with async_session_maker() as db:
            if not order_id:
                return False
            else:
                order = await db.execute(select(Orders).where(Orders.id == order_id).
                                         options(selectinload(cls.model.customer)).
                                         options(selectinload(cls.model.items))
                                         )
                order = order.scalars().first()
                return order

    @classmethod
    async def status_order(cls, status, order_id):
        async with async_session_maker() as db:
            if not order_id or not status:
                return False
            else:
                await db.execute(update(Orders).where(Orders.id == order_id).values(status=status))

                await db.commit()
                return True

    @classmethod
    async def get_all_info_order(cls, order_id):
        async with async_session_maker() as db:
            if not order_id:
                return False
            order = await db.execute(select(Orders).where(Orders.id == order_id).
                                     options(selectinload(cls.model.customer)).
                                     options(selectinload(cls.model.items)).
                                     options(selectinload(cls.model.components)).
                                     options(selectinload(cls.model.comments)))
            order = order.scalars().first()
            return order

    @classmethod
    async def get_all_info_order_users(cls, order_id):
        async with async_session_maker() as db:
            if not order_id:
                return False
            order = await db.execute(select(Orders).where(Orders.id == order_id).
                                     options(selectinload(cls.model.customer)).
                                     options(selectinload(cls.model.items)).
                                     options(selectinload(cls.model.components)).
                                     options(selectinload(cls.model.comments)).
                                     options(selectinload(cls.model.user)))
            order = order.scalars().first()
            return order

    @classmethod
    async def get_all_orders_to_customer(cls, customer_id):
        async with async_session_maker() as db:
            if not customer_id:
                return False
            orders = await db.execute(select(Orders).where(Orders.customer_id == customer_id))
            orders = orders.scalars().all()
            if not isinstance(orders, list):
                return [orders]
            else:
                return orders
