import contextlib
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .session import async_session


@contextlib.asynccontextmanager
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = async_session()
    try:
        if not session.in_transaction():
            await session.begin()
        yield session
        await session.commit()
    except SQLAlchemyError as _ex:
        await session.rollback()
        raise _ex
    finally:
        await session.close()
