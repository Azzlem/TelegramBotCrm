from datetime import datetime

from sqlalchemy import ForeignKey, DateTime

from base import Base

from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.comments import Comments
from models.components import Components
from models.items import Items


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)
    items: Mapped[Items] = relationship('Items', backref='items')
    components: Mapped[Components] = relationship('Components', backref='components')
    comments: Mapped[Comments] = relationship('Comments', backref='comments')

    created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)



