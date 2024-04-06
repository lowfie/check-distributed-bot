from decimal import Decimal
from datetime import datetime

from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

from src.config import config
from src.database.base import Base


class TotalDistribution(Base):
    created_at: Mapped[int] = mapped_column(BigInteger, default=datetime.now().timestamp())

    input_aix: Mapped[Decimal]
    distributed_aix: Mapped[Decimal]
    swapped_eth: Mapped[Decimal]
    distributed_eth: Mapped[Decimal]

    tx_hash: Mapped[str] = Column(String(1024), unique=True)

    def __str__(self) -> str:
        return f"Tx hash: {self.tx_hash}"

    @hybrid_property
    async def network_transaction(self) -> dict:
        return await config.web3.w3.eth.get_transaction(self.tx_hash)
