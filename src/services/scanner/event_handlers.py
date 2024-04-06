import abc
import logging

from web3.contract.async_contract import AsyncContractEvent
from web3.types import EventData

from src.config import config
from src.database.actions import db_session
from src.services import total_distribution
from src.services.scanner.event_schemas import (
    EventBaseSchema,
    TotalDistributionEventSchema
)


class EventHandler(abc.ABC):
    def __init__(
        self, event: AsyncContractEvent, event_schema: EventBaseSchema
    ) -> None:
        self.event = event
        self.event_schema = event_schema

    async def handle_event(self):
        raise NotImplementedError

    async def handle(self, event: EventData):
        self.data = self.event_schema(**event)
        await self.handle_event()


class TotalDistributionEventHandler(EventHandler):
    data: TotalDistributionEventSchema

    async def handle_event(self):
        async with db_session() as db:
            block = await config.web3.w3.eth.get_block(self.data.block_number)

            await total_distribution.create(
                db=db,
                input_aix=self.data.args.input_aix_amount,
                distributed_aix=self.data.args.distributed_aix_amount,
                swapped_eth=self.data.args.swapped_eth_amount,
                distributed_eth=self.data.args.distributed_eth_amount,
                tx_hash=self.data.transaction_hash.hex(),
                created_at=block.get("timestamp"),
            )
