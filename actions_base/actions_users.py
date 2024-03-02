from sqlalchemy import select

from base import async_session_maker
from formatting.user_formatting import UserFormatter
from models.users import Users


class UserActions:
    model = Users

    @classmethod
    async def add_user(cls, data):
        async with async_session_maker() as db:
            user = await UserFormatter.convert_to_add(data)
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
    async def get_all_users(cls):
        async with async_session_maker() as db:
            users = await db.execute(select(cls.model))
            users = users.scalars().all()
            return users
