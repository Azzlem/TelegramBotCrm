from sqlalchemy import select
from sqlalchemy.orm import selectinload

from base import async_session_maker
from models.models import Orders, Users


class OrdersActions:
    model = Orders

    @classmethod
    async def add_orders(cls, data):
        async with async_session_maker() as session:
            order = Orders(**data)
            session.add(order)
            await session.commit()

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
