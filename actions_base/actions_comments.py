from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.models import Comments
from base import async_session_maker


class CommentActions:
    model = Comments

    @classmethod
    async def create(cls, comment, order_id: int, user_id: int) -> Comments:
        comment = cls.model(text=comment, order_id=order_id, owner_id=user_id)
        async with async_session_maker() as db:
            db.add(comment)
            await db.commit()
            return comment

    @classmethod
    async def get_comments_by_order_id(cls, order_id: int) -> List[Comments]:
        async with async_session_maker() as db:
            comments = await db.execute(select(cls.model).where(cls.model.order_id == order_id).
                                        options(selectinload(cls.model.owner)))
            comments = comments.scalars().all()
            return comments
