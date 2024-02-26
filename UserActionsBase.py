from sqlalchemy import delete, update, select
import permissions
from base import async_session_maker
from order.models import User


class UserService:
    model = User

    @classmethod
    async def create(cls, data: dict) -> str:
        async with async_session_maker() as db_session:
            try:
                user = cls.model(**data)
                db_session.add(user)
                await db_session.commit()
                return user.name
            except:
                print("An error occurred while creating")
                return "Error creating"

    @classmethod
    async def delete(cls, tg_user_id: int, user_id: int) -> bool:
        if await permissions.perm_admin(tg_user_id):
            try:
                async with async_session_maker() as db_session:
                    await db_session.execute(delete(cls.model).where(cls.model.id == user_id))
                    await db_session.commit()
                    return True
            except:
                print("An error occurred while")
                return False
        else:
            print("You do not have permission to delete this user")
            return False

    @classmethod
    async def update(cls, tg_user_id: int, data: dict) -> bool:
        if await permissions.perm_admin(tg_user_id):
            try:
                data_temp = data.pop("order_id")
                async with async_session_maker() as db_session:
                    await db_session.execute(update(cls.model).where(cls.model.id == data_temp).values(**data))
                    await db_session.commit()
                    return True
            except:
                print("An error occurred while")
                return False

    @classmethod
    async def valid_user(cls, user_id):
        async with async_session_maker() as db_session:
            user = await db_session.execute(select(cls.model).where(cls.model.tg_user_id == user_id))
            a = user.all()
            if not a:
                return False
            b = a[0][0].status
            if b == 1:
                return "user"
            if b == 2:
                return "admin"
            return False