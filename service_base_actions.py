from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert
from base import async_session_maker
from order.models import User, Comment, Order
from utils_format import format_data_user_set, format_valid_user


class ServiceBaseActions:

    @classmethod
    async def add_user(cls, data):
        async with async_session_maker() as db:
            data = await format_data_user_set(data)
            await db.execute(insert(User).values(**data))
            await db.commit()
            return True

    @classmethod
    async def get_user(cls, data):
        async with async_session_maker() as db:
            user = await db.execute(select(User).filter_by(tg_user_id=data.id))
            if user:
                return user.scalars().first()
            return False

    @classmethod
    async def get_all_users(cls):
        async with async_session_maker() as db:
            users = await db.execute(select(User))
            users = users.scalars().all()
            return users

    @classmethod
    async def delete_user(cls, data):
        async with async_session_maker() as db:
            await db.execute(delete(User).filter_by(id=data['user_id']))
            await db.commit()

    @classmethod
    async def change_perms_user(cls, data):
        async with async_session_maker() as db:
            await db.execute(update(User).where(User.id == int(data['user_id'])).values(status=int(data['status'])))
            await db.commit()
            return True

    @classmethod
    async def valid_user(cls, data):
        async with async_session_maker() as db:
            user = await db.execute(select(User).where(User.tg_user_id == data))
            user = user.scalars().all()
            answer = await format_valid_user(user)
            return answer


class ServiceBaseActionsOrder:

    @classmethod
    async def order(cls, order_id):
        async with async_session_maker() as db:
            order = await db.execute(select(Order).filter_by(id=order_id['order_id']))
            order = order.scalars().first()
            comments = await db.execute(select(Comment).filter_by(order_id=order.id))
            comments = comments.scalars().all()
            return order, comments

