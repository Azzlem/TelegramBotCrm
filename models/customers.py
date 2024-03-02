from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Sale(Enum):
    VISITOR = 0
    BRONZE = 10
    SILVER = 20
    GOLD = 25
    PLATINUM = 30


class Customers(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=True)
    sales: Mapped[Sale] = mapped_column(default=Sale.VISITOR)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)
