from typing import List, Type, Any

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from base import async_session_maker, Base
from models.enums import Status
from models.models import Orders, Users
from permission import is_owner_admin, is_user


class OrdersActions:
    model = Orders

    @classmethod
    async def add_orders(cls, data: dict) -> Orders:
        async with async_session_maker() as session:
            order = cls.model(**data)
            session.add(order)
            await session.commit()
            return order

    @classmethod
    async def create_order(cls, customer_id: int, user_id: int) -> Orders:
        async with async_session_maker() as session:
            if user_id == "None":
                order = Orders(customer_id=customer_id)
            else:
                order = Orders(customer_id=customer_id, user_id=user_id)

            session.add(order)
            await session.commit()
            return order

    @classmethod
    async def create_orders_without_user(cls, customer_id: int) -> Orders:
        async with async_session_maker() as session:
            order = Orders(customer_id=customer_id)
            session.add(order)
            await session.commit()
            return order

    @classmethod
    async def get_orders_with_customer(cls, user: Users) -> List[Orders]:
        async with async_session_maker() as db:
            orders = await db.execute(select(cls.model).where(cls.model.user_id == user.id).
                                      options(selectinload(cls.model.customer)))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_all_orders(cls) -> List[Orders]:
        async with async_session_maker() as db:
            orders = await db.execute(select(cls.model))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_all_orders_with_customer(cls) -> List[Orders]:
        async with async_session_maker() as db:
            orders = await db.execute(select(cls.model).
                                      options(selectinload(cls.model.customer)))
            orders = orders.scalars().all()
            return orders

    @classmethod
    async def get_all_orders_accepted(cls, user: Users, status: Status) -> List[Orders]:
        async with async_session_maker() as db:
            query = select(cls.model).filter_by(status=status)
            if await is_owner_admin(user):
                query = query.options(selectinload(cls.model.customer)).options(selectinload(cls.model.items))
            else:
                query = query.filter_by(user_id=user.id).options(selectinload(cls.model.customer)).options(
                    selectinload(cls.model.items))
            orders = await db.execute(query)
            return orders.scalars().all()

    @classmethod
    async def appoint_user_to_order(cls, user_id: int, order_id: int) -> bool:
        async with async_session_maker() as db:
            if not user_id:
                return False
            try:
                await db.execute(
                    update(cls.model).where(cls.model.id == order_id).values(user_id=user_id)
                )
                await db.commit()
                return True
            except Exception as e:
                # Логирование или обработка исключения
                raise e

    @classmethod
    async def get_order(cls, order_id: int) -> bool | Any:
        async with async_session_maker() as db:
            if not order_id:
                return False
            else:
                order = await db.execute(select(cls.model).where(cls.model.id == order_id).
                                         options(selectinload(cls.model.customer)).
                                         options(selectinload(cls.model.items))
                                         )
                order = order.scalars().first()
                return order

    @classmethod
    async def status_order(cls, status: Status, order_id: int) -> bool:
        async with async_session_maker() as db:
            if not order_id or not status:
                return False
            else:
                await db.execute(update(cls.model).where(cls.model.id == order_id).values(status=status))
                await db.commit()
                return True

    @classmethod
    async def get_all_info_order(cls, order_id: int) -> List[Orders] | Any:
        async with async_session_maker() as db:
            if not order_id:
                return False
            order = await db.execute(select(cls.model).where(cls.model.id == order_id).
                                     options(selectinload(cls.model.customer)).
                                     options(selectinload(cls.model.items)).
                                     options(selectinload(cls.model.components)).
                                     options(selectinload(cls.model.comments)))
            order = order.scalars().first()
            return order

    @classmethod
    async def get_all_info_order_users(cls, order_id: int) -> List[Users] | Any:
        async with async_session_maker() as db:
            if not order_id:
                return False
            order = await db.execute(select(cls.model).where(cls.model.id == order_id).
                                     options(selectinload(cls.model.customer)).
                                     options(selectinload(cls.model.items)).
                                     options(selectinload(cls.model.components)).
                                     options(selectinload(cls.model.comments)).
                                     options(selectinload(cls.model.user)))
            order = order.scalars().first()
            return order

    @classmethod
    async def get_all_orders_to_customer(cls, customer_id: int) -> List[Orders] | Any:
        async with async_session_maker() as db:
            if not customer_id:
                return False
            orders = await db.execute(select(cls.model).where(cls.model.customer_id == customer_id).
                                      options(selectinload(cls.model.customer)).
                                      options(selectinload(cls.model.items)))
            orders = orders.scalars().all()
            if not isinstance(orders, list):
                return [orders]
            else:
                return orders
