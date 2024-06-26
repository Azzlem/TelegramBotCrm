from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from settings import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.db_url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)