from typing import List

from sqlalchemy import select, update

from base import async_session_maker
from dataclass import DataClass
from models.models import Customers


class CustomerActions:
    model = Customers

    @classmethod
    async def add_customer(cls, data) -> Customers:
        customer = cls.model(
            fullname=data.fullname,
            phone=data.phone,
            address=data.address
        )
        async with async_session_maker() as db:
            db.add(customer)
            await db.commit()
            return customer

    @classmethod
    async def get_customers(cls) -> List[Customers]:
        async with async_session_maker() as db:
            customers = await db.execute(select(cls.model))
            customers = customers.scalars().all()
            return customers

    @classmethod
    async def get_customers_for_fullname(cls, full_name: str) -> List[Customers]:
        async with async_session_maker() as db:
            string_search = f'%{full_name}%'
            customers = await db.execute(select(cls.model).filter(cls.model.fullname.ilike(string_search)))
            customers = customers.scalars().all()
            return customers

    @classmethod
    async def get_customer(cls, customer_id: int) -> Customers:
        async with async_session_maker() as db:
            customer = await db.execute(select(cls.model).where(cls.model.id == customer_id))
            customer = customer.scalars().first()
            return customer

    @classmethod
    async def edit_customer(cls, data) -> None:
        customer_id = data.pop('customer_id')
        async with async_session_maker() as db:
            await db.execute(update(cls.model).where(cls.model.id == customer_id).values(**data))
            await db.commit()

    @classmethod
    async def get_customer_by_phone(cls, phone: int) -> Customers:
        async with async_session_maker() as db:
            customer = await db.execute(select(cls.model).where(cls.model.phone == phone))
            customer = customer.scalars().first()
            return customer

    @classmethod
    async def add_customer_in_order(cls, fullname: str, phone: int, address: str) -> Customers:
        customer = cls.model(fullname=fullname, phone=phone, address=address)
        async with async_session_maker() as db:
            db.add(customer)
            await db.commit()
            return customer

    @classmethod
    async def custom_add_customer(cls, customer: Customers) -> Customers:
        async with async_session_maker() as db:
            db.add(customer)
            await db.commit()
            return customer
