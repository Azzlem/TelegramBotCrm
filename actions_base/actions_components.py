from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.models import Components
from base import async_session_maker


class ComponentActions:
    model = Components

    @classmethod
    async def create(cls, name, path_photo, order_id, price):
        comment = cls.model(name=name, path_photo=path_photo, order_id=order_id, price=price)
        async with async_session_maker() as db:
            db.add(comment)
            await db.commit()
            return comment

    @classmethod
    async def get(cls, order_id):
        async with async_session_maker() as db:
            components = await db.execute(select(cls.model).where(cls.model.order_id == order_id))
            if components:
                return components.scalars().all()
            else:
                return None

