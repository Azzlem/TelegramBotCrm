from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Role(Enum):
    ADMIN = 1
    USER = 2
    OWNER = 0
    REGISTERED = 3


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
