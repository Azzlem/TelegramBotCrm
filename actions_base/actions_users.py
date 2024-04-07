from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from base import async_session_maker
from formatting.user_formatting import UserFormatter
from models.models import Users


class UserActions:
    model = Users

    @classmethod
    async def add_user(cls, data) -> Users:
        async with async_session_maker() as db:
            user: cls.model = await UserFormatter.convert_to_add(data)
            db.add(user)
            await db.commit()
            return user

    @classmethod
    async def get_user(cls, data):
        async with async_session_maker() as db:
            user = await db.execute(select(cls.model).filter_by(telegram_id=data.id))
            if user:
                return user.scalars().first()
            return False

    @classmethod
    async def get_user_from_id(cls, data):
        async with async_session_maker() as db:
            user = await db.execute(select(cls.model).filter_by(id=data.id))
            if user:
                return user.scalars().first()
            return False

    @classmethod
    async def get_all_users(cls):
        async with async_session_maker() as db:
            users = await db.execute(select(cls.model))
            users = users.scalars().all()
            return users

    @classmethod
    async def get_all_users_with_count_orders(cls):
        async with async_session_maker() as db:
            users = await db.execute(select(cls.model).options(selectinload(cls.model.orders)))
            users = users.scalars().all()
            return users

    @classmethod
    async def delete_user(cls, data):

        async with async_session_maker() as db:
            await db.execute(delete(cls.model).filter_by(id=int(data['user_id'])))
            await db.commit()

    @classmethod
    async def update_user(cls, data):
        async with async_session_maker() as db:
            await db.execute(update(cls.model).filter_by(id=int(data['user_id'])).values(role=data['role']))
            await db.commit()
# class UserActions:
#     model = Users
#
#     @classmethod
#     async def add_user(cls, data) -> Users:
#         async with async_session_maker() as db:
#             user = await UserFormatter.convert_to_add(data)
#             db.add(user)
#             await db.commit()
#             return user
#
#     @classmethod
#     async def _get_user(cls, query_value, field_name="telegram_id"):  # Common logic for user retrieval
#         async with async_session_maker() as db:
#             user = await db.execute(select(cls.model).filter_by(**{field_name: query_value}))
#             return user.scalars().first()
#
#     @classmethod
#     async def get_user(cls, data):
#         return await cls._get_user(data.id)
#
#     @classmethod
#     async def get_user_from_id(cls, data):
#         return await cls._get_user(data.id, "id")
#
#     @classmethod
#     async def get_all_users(cls):
#         async with async_session_maker() as db:
#             users = await db.execute(select(cls.model))
#             return users.scalars().all()
#
#     @classmethod
#     async def get_all_users_with_count_orders(cls):
#         async with async_session_maker() as db:
#             users = (
#                 await db.execute(select(cls.model).options(selectinload(cls.model.orders)))
#             ).scalars()
#             return users  # No need to call .all() on a scalars result
#
#     @classmethod
#     async def delete_user(cls, data):
#         async with async_session_maker() as db:
#             await db.execute(delete(cls.model).filter_by(id=int(data['user_id'])))
#             await db.commit()
#
#     @classmethod
#     async def update_user(cls, data):
#         async with async_session_maker() as db:
#             await db.execute(
#                 update(cls.model).filter_by(id=int(data['user_id'])).values(role=data['role'])
#             )
#             await db.commit()

