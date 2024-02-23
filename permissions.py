import asyncio

from sqlalchemy import select

from base import async_session_maker
from order.models import User


async def perm_admin(tg_user_id):
    async with async_session_maker() as db_session:
        user = await db_session.execute(select(User).where(User.tg_user_id == tg_user_id))
        if user.scalars().first().status == 2:
            return True
        return False


