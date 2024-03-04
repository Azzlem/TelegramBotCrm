from datetime import datetime
from enum import Enum
from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base


class Role(Enum):
    ADMIN = 1
    USER = 2
    OWNER = 0
    REGISTERED = 3


class Sale(Enum):
    VISITOR = 0
    BRONZE = 10
    SILVER = 20
    GOLD = 25
    PLATINUM = 30


class Vendor(Enum):
    UNKNOWN = 0
    CANON = 0
    DELI = 1
    HP = 2
    HUAWEI = 3
    KYOCERA = 4
    PANTUM = 5
    RICOH = 6
    XEROX = 7
    SHARP = 8
    BROTHER = 9
    EPSON = 10
    DEXP = 11
    KONICA = 12
    XIAOMI = 13
    ALGOTEX = 14
    SUNICA = 15
    OKI = 16
    PANASONIC = 17
    MITA = 18
    SECRET_KYOCERA = 19


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(64), index=True)
    fullname: Mapped[str]
    phone: Mapped[int] = mapped_column(BigInteger, index=True, nullable=True)
    role: Mapped[Role] = mapped_column(default=Role.REGISTERED)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

    orders: Mapped[list["Orders"]] = relationship(back_populates='user')


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)

    items: Mapped[list["Items"]] = relationship(back_populates='order')
    components: Mapped[list["Components"]] = relationship(back_populates='order')
    comments: Mapped[list["Comments"]] = relationship(back_populates='order')

    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

    user: Mapped["Users"] = relationship(back_populates='orders')
    customer: Mapped["Customers"] = relationship(back_populates='orders')


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

    orders: Mapped[list["Orders"]] = relationship(back_populates="customer")


class Items(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor: Mapped[Vendor] = mapped_column(default=Vendor.UNKNOWN)
    model: Mapped[str] = mapped_column(nullable=True)
    defect: Mapped[str] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

    order: Mapped["Orders"] = relationship(back_populates="items")


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='SET NULL'), nullable=True)

    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

    order: Mapped["Orders"] = relationship(back_populates="comments")


class Components(Base):
    __tablename__ = 'components'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

    order: Mapped["Orders"] = relationship(back_populates="components")
