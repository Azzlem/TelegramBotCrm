from base import async_session_maker
from models.models import Items


class ItemsActions:
    model = Items

    @classmethod
    async def add_item(cls, data):
        print(data)
        item = cls.model(**data)
        async with async_session_maker() as db:
            db.add(item)
            await db.commit()
