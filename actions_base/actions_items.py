from base import async_session_maker
from models.models import Items, Vendor


class ItemsActions:
    model = Items

    @classmethod
    async def add_item(cls, data):
        item = cls.model(**data)
        async with async_session_maker() as db:
            db.add(item)
            await db.commit()

    @classmethod
    async def add_item_to_order(cls, vendor, model, defect, order_id):
        async with async_session_maker() as db:
            item = cls.model(vendor=vendor, model=model, defect=defect, order_id=order_id)
            db.add(item)
            await db.commit()
            return item
