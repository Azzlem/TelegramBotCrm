import asyncio
from datetime import datetime
from typing import Annotated
from sqlalchemy import ForeignKey, BigInteger, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from base import Base, async_session_maker

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = 'user'

    id: Mapped[intpk]
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str]
    status: Mapped[int] = mapped_column(default=0)


class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[intpk]
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id', ondelete='CASCADE'), nullable=True)


class Order(Base):
    __tablename__ = 'order'
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    client_name: Mapped[str]
    client_phone: Mapped[str]
    device: Mapped[str]
    mulfunction: Mapped[str]
    comments: Mapped[Comment] = relationship('Comment', backref='customer')


# class Customer(Base):
#     __tablename__ = 'customer'
#
#     id: Mapped[intpk]
#     first_name: Mapped[str]
#     last_name: Mapped[str]
#     email: Mapped[str] = mapped_column(nullable=True)
#     phone: Mapped[str] = mapped_column(nullable=False)
#     address: Mapped[str] = mapped_column(nullable=True)
#     comments: Mapped[Comment] = relationship('Comment', backref='customer')


