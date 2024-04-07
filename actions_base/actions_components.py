from sqlalchemy import select

from models.models import Components
from base import async_session_maker


class ComponentActions:
    model = Components

    @classmethod
    async def create(cls, name, path_photo: str, order_id: int, price: int) -> Components:
        component = cls.model(name=name, path_photo=path_photo, order_id=order_id, price=price)
        async with async_session_maker() as db:
            db.add(component)
            await db.commit()
            return component

    @classmethod
    async def get(cls, order_id: int) -> Components | None:
        async with async_session_maker() as db:
            components = await db.execute(select(cls.model).where(cls.model.order_id == order_id))
            if components:
                return components.scalars().all()
            else:
                return None

