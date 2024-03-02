from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Components(Base):
    __tablename__ = 'components'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)
