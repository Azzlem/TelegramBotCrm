from sqlalchemy import select, update

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

    @classmethod
    async def get_customers(cls):
        async with async_session_maker() as db:
            customers = await db.execute(select(Customers))
            customers = customers.scalars().all()
            return customers

    @classmethod
    async def get_customers_for_fullname(cls, full_name: str):
        async with async_session_maker() as db:
            string_search = f'%{full_name}%'
            customers = await db.execute(select(Customers).filter(Customers.fullname.ilike(string_search)))
            customers = customers.scalars().all()
            return customers

    @classmethod
    async def get_customer(cls, data):
        async with async_session_maker() as db:
            customer = await db.execute(select(Customers).where(Customers.id == data['customer_id']))
            customer = customer.scalars().first()
            return customer

    @classmethod
    async def edit_customer(cls, data):
        customer_id = data.pop('customer_id')

        async with async_session_maker() as db:
            await db.execute(update(Customers).where(Customers.id == customer_id).values(**data))
            await db.commit()

    @classmethod
    async def get_customer_by_phone(cls, data):
        async with async_session_maker() as db:
            customer = await db.execute(select(Customers).where(Customers.phone == data))
            customer = customer.scalars().first()
            return customer
