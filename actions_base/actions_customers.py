from base import async_session_maker
from models.models import Customers


class CustomerActions:
    model = Customers

    @classmethod
    async def add_customer(cls, data):
        customer = Customers(**data)
        async with async_session_maker() as db:
            db.add(customer)
            await db.commit()
            return customer
