from web3.types import EventData

from src.config import config
from src.services.redis import redis

from .base import Scanner
from .event_handlers import EventHandler


class EventScanner(Scanner):
    def __init__(self, event_handler: EventHandler):
        self.event_handler = event_handler
        self.name = (
            f"{self.event_handler.event.address}-{self.event_handler.event.event_name}"
        )
        super().__init__(name=self.name)

    async def get_last_block_processed(self) -> int:
        block_num = await redis.get_int(self.name)
        if not block_num:
            block_num = await config.web3.w3.eth.block_number
            await self.save_last_block_processed(block_num=block_num)
        return block_num

    async def save_last_block_processed(self, block_num: int) -> None:
        await redis.set_int(key=self.name, value=block_num)

    async def scan(self, from_block: int, to_block: int) -> None:
        events: list[EventData] = await self.event_handler.event.get_logs(
            fromBlock=from_block, toBlock=to_block
        )
        for event in events:
            self.logger.info(f"event received {event}")
            await self.event_handler.handle(event)
