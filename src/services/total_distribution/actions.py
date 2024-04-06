from hexbytes import HexBytes
from datetime import datetime, timedelta

from sqlalchemy import func, select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.services.total_distribution.types import TotalDistributedInitial


async def create(
        db: AsyncSession,
        input_aix: int,
        distributed_aix: int,
        swapped_eth: int,
        distributed_eth: int,
        tx_hash: str | HexBytes,
        created_at: int | None
) -> models.TotalDistribution:
    total_distributed = await models.TotalDistribution.create(
        db=db,
        input_aix=input_aix,
        distributed_aix=distributed_aix,
        swapped_eth=swapped_eth,
        distributed_eth=distributed_eth,
        tx_hash=tx_hash,
        created_at=created_at
    )
    return total_distributed


async def statistic(
        db: AsyncSession,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0
):
    last_day = datetime.now() - timedelta(days=days, hours=hours, minutes=minutes)
    stmt = (
        select(
            func.sum(models.TotalDistribution.input_aix).label("input_aix"),
            func.sum(models.TotalDistribution.distributed_aix).label("distributed_aix"),
            func.sum(models.TotalDistribution.swapped_eth).label("swapped_eth"),
            func.sum(models.TotalDistribution.distributed_eth).label("distributed_eth"),
        )
        .where(models.TotalDistribution.created_at >= last_day.timestamp())
    )
    instance = await db.execute(stmt)
    return instance.first()


async def get_by(db: AsyncSession, **kwargs):
    return await models.TotalDistribution.get_by(db=db, **kwargs)


async def first_or_last_instance(db: AsyncSession, initial: TotalDistributedInitial):
    last_day = datetime.now() - timedelta(days=1)

    if initial not in list(TotalDistributedInitial):
        return None

    if initial == TotalDistributedInitial.LAST:
        ordered = asc(models.TotalDistribution.created_at)
    else:
        ordered = desc(models.TotalDistribution.created_at)

    stmt = (
        select(models.TotalDistribution)
        .where(models.TotalDistribution.created_at >= last_day.timestamp())
        .order_by(ordered)
    )
    return await db.scalar(stmt)
