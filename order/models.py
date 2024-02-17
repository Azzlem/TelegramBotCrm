from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from base import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = 'user'

    id: Mapped[intpk]
    tg_user_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)


class Order(Base):
    __tablename__ = 'order'
    id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(ForeignKey('user.id'))
    client_name: Mapped[str]
    client_phone: Mapped[str]
    device: Mapped[str]
    mulfunction: Mapped[str]



