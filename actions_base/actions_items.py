from typing import List

from sqlalchemy import select

from base import async_session_maker
from models.models import Items, Vendor


class ItemsActions:
    model = Items

    @classmethod
    async def add_item(cls, data: dict) -> Items:
        item = cls.model(**data)
        async with async_session_maker() as db:
            db.add(item)
            await db.commit()
            return item

    @classmethod
    async def add_item_to_order(cls, vendor: str, model: str, defect: str, order_id: int) -> Items:
        async with async_session_maker() as db:
            item = cls.model(vendor=vendor, model=model, defect=defect, order_id=order_id)
            db.add(item)
            await db.commit()
            return item

    @classmethod
    async def get_items_by_order_id(cls, order_id: int) -> List[Items]:
        async with async_session_maker() as db:
            items = await db.execute(select(cls.model).where(cls.model.order_id == order_id))
            items = items.scalars().all()
            if not isinstance(items, list):
                return [items]
            else:
                return items
