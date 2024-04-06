from asyncio import current_task

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import async_sessionmaker as _async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

engine = create_async_engine(
    settings.POSTGRES_DSN,
    echo=False,
    echo_pool=False,
    pool_size=150,
    max_overflow=10,
    pool_pre_ping=True
)

async_session_factory = _async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)
async_session = async_scoped_session(async_session_factory, scopefunc=current_task)
