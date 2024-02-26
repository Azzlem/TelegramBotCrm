from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert

from base import async_session_maker
from order.models import User
from utils_format import format_data_user_set, format_valid_user


class ServiceBaseActions:
    db = async_session_maker()

    @classmethod
    async def add_user(cls, data):
        data = await format_data_user_set(data)
        await cls.db.execute(insert(User).values(**data))
        await cls.db.commit()
        return True

    @classmethod
    async def get_user(cls, data):
        user = await cls.db.execute(select(User).filter_by(tg_user_id=data.id))
        if user:
            return user.scalars().first()
        return False

    @classmethod
    async def get_all_users(cls):
        users = await cls.db.execute(select(User))
        users = users.scalars().all()
        return users

    @classmethod
    async def delete_user(cls, data):
        await cls.db.execute(delete(User).filter_by(id=data['user_id']))
        await cls.db.commit()

    @classmethod
    async def change_perms_user(cls, data):
        await cls.db.execute(update(User).where(User.id == int(data['user_id'])).values(status=int(data['status'])))
        return True

    @classmethod
    async def valid_user(cls, data):
        user = await cls.db.execute(select(User).where(User.tg_user_id == data))
        user = user.scalars().all()
        answer = await format_valid_user(user)
        return answer



