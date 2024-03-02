from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


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
