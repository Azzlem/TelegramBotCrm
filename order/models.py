from typing import Annotated
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from base import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = 'user'

    id: Mapped[intpk]
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str]
    status: Mapped[int] = mapped_column(default=0)


class Order(Base):
    __tablename__ = 'order'
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    client_name: Mapped[str]
    client_phone: Mapped[str]
    device: Mapped[str]
    mulfunction: Mapped[str]



