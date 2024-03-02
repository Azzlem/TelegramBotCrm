from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id', ondelete='SET NULL'), nullable=True)

    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)
