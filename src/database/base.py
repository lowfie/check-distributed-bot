from datetime import datetime, UTC
from typing import TypeVar, Type, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, BigInteger
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from src.utils.helpers import to_underscore_lower_case

T = TypeVar("T", bound=DeclarativeBase)


class Base(DeclarativeBase):
    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now(UTC).replace(tzinfo=None), default=datetime.now(UTC).replace(tzinfo=None))

    @declared_attr.directive
    def __tablename__(self):
        return to_underscore_lower_case(self.__name__)

    @classmethod
    async def get(cls: Type[T] | "Base", db: AsyncSession, id: int) -> T | None:
        stmt = select(cls).where(cls.id == id)
        instance = await db.scalar(stmt)
        return instance

    @classmethod
    async def get_by(cls: Type[T] | "Base", db: AsyncSession, **kwargs) -> T | None:
        stmt = select(cls).filter_by(**kwargs)
        instance = await db.scalar(stmt)
        return instance

    @classmethod
    async def get_all(cls: Type[T] | "Base", db: AsyncSession) -> Sequence[T]:
        stmt = select(cls)
        instances = await db.scalars(stmt)
        return instances.all()

    @classmethod
    async def get_multi(
            cls: Type[T] | "Base",
            db: AsyncSession,
            limit: int | None = None,
            skip: int | None = None, **kwargs
    ) -> Sequence[T]:
        stmt = select(cls).filter_by(**kwargs).offset(skip).limit(limit)
        instance = await db.scalars(stmt)
        return instance.all()

    @classmethod
    async def delete(cls: Type[T] | "Base", db: AsyncSession, id: int) -> None:
        stmt = delete(cls).where(cls.id == id)
        await db.execute(stmt)
        await db.flush()

    @classmethod
    async def delete_by(cls: Type[T] | "Base", db: AsyncSession, **kwargs) -> None:
        stmt = delete(cls).filter_by(**kwargs)
        await db.execute(stmt)
        await db.flush()

    @classmethod
    async def create(cls: Type[T] | "Base", db: AsyncSession, **kwargs) -> T:
        instance = cls(**kwargs)
        db.add(instance)
        await db.flush()
        return instance

    @classmethod
    async def bulk_create(cls: Type[T] | "Base", db: AsyncSession, dict_values: list[dict]) -> None:
        instances = [cls(**values) for values in dict_values]
        db.add_all(instances)
        await db.flush()

    @classmethod
    async def update(cls: Type[T] | "Base", db: AsyncSession, id: int, **kwargs):
        stmt = update(cls).values(**kwargs).where(cls.id == id)
        await db.execute(stmt)
        await db.flush()

    @classmethod
    async def get_or_create(
            cls: Type[T] | "Base",
            db: AsyncSession,
            defaults: dict | None = None,
            **kwargs,
    ) -> tuple[T, bool]:
        instance = await cls.get_by(db=db, **kwargs)
        if instance:
            return instance, False
        else:
            params = dict(defaults or {}, **kwargs)
            return await cls.create(db=db, **params), True
