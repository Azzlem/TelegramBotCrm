from sqlalchemy import select, update, delete
from base import async_session_maker
from order.models import Order, User
from permissions import perm_admin


class OrderService:
    model = Order

    @classmethod
    async def get_orders(cls, tg_user_id: int) -> list:

        if await perm_admin(tg_user_id):
            async with async_session_maker() as db_session:
                order = await db_session.execute(select(cls.model))
                return order.scalars().all()
        else:
            async with async_session_maker() as db_session:
                user = await db_session.execute(select(User).where(User.tg_user_id == tg_user_id))
                order = await db_session.execute(select(cls.model).where(cls.model.user_id == user.scalars().first().id))
                return order.scalars().all()

    @classmethod
    async def create_order(cls, data: dict) -> bool:
        async with async_session_maker() as db_session:
            try:
                order = cls.model(**data)
                db_session.add(order)
                await db_session.commit()
                return True
            except:
                await db_session.rollback()
                return False

    @classmethod
    async def update_order(cls, data: dict) -> bool:
        async with async_session_maker() as db_session:
            data_temp = data.pop("order_id")
            try:
                data_temp = data.pop("order_id")
                await db_session.execute(update(cls.model).where(cls.model.id == data_temp).values(**data))
                await db_session.commit()
                return True
            except:
                await db_session.rollback()
                print("error updating order")
                return False

    @classmethod
    async def delete_order(cls, order_id: int, tg_user_id: int) -> bool:
        if await perm_admin(tg_user_id):
            async with async_session_maker() as db_session:
                try:
                    await db_session.execute(delete(cls.model).where(cls.model.id == order_id))
                    await db_session.commit()
                    return True
                except:
                    await db_session.rollback()
                    return False
        else:
            return False

