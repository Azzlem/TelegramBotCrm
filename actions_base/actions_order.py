from sqlalchemy import select
from sqlalchemy.orm import selectinload

from base import async_session_maker
from models.models import Orders


class OrdersActions:
    model = Orders

    @classmethod
    async def get_orders(cls, data):
        async with async_session_maker() as db:
            orders = await db.execute(select(Orders).where(Orders.user_id == data.id))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_orders_with_customer(cls, data):
        async with async_session_maker() as db:
            orders = await db.execute(select(Orders).where(Orders.user_id == data.id).options(selectinload(cls.model.customer)))

            orders = orders.scalars().all()


            return orders

