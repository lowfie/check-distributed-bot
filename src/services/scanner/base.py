import asyncio
import logging
from abc import ABC, abstractmethod

from src.config import config
from src.services.scanner.decorators import async_never_fall


class Scanner(ABC):
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    @abstractmethod
    async def get_last_block_processed(self) -> int:
        ...

    @abstractmethod
    async def save_last_block_processed(self, block_num: int) -> None:
        ...

    @abstractmethod
    async def scan(self, from_block: int, to_block: int) -> None:
        ...

    @async_never_fall
    async def start(self):
        max_filter_length = config.scanner.maximum_scanning_blocks

        while True:
            last_network_block = await config.web3.w3.eth.block_number
            last_block_processed = await self.get_last_block_processed()
            last_block_confirmed = last_network_block - config.scanner.confirmation_blocks

            if last_block_processed >= last_block_confirmed:
                self.logger.info(
                    f"waiting {last_block_processed - last_block_confirmed} blocks..."
                )
                await asyncio.sleep(10)
                continue

            if last_block_confirmed - last_block_processed > max_filter_length:
                to_block = last_block_processed + max_filter_length
                sleep_secs = config.scanner.speedy_polling_interval
            else:
                to_block = last_block_confirmed
                sleep_secs = config.scanner.polling_interval

            from_block = last_block_processed + 1

            self.logger.info(
                f"scanning [{from_block}, {to_block}] / {last_block_confirmed}"
            )

            await self.scan(from_block, to_block)

            last_block_processed = to_block
            await self.save_last_block_processed(last_block_processed)
            await asyncio.sleep(sleep_secs)
