import asyncio

import uvloop
from web3.contract.async_contract import AsyncContract

from src.config import config
from src.services.scanner.event_scanner import EventScanner
from src.services.scanner.event_schemas import TotalDistributionEventSchema
from src.services.scanner.event_handlers import TotalDistributionEventHandler


async def run_event_scanners():
    # TODO: move instance contract from here
    aix_treasury: AsyncContract = config.web3.w3.eth.contract(
        address=config.contracts.aix_treasury, abi=config.abi.aix_treasury
    )

    event_handlers = [
        TotalDistributionEventHandler(
            event=aix_treasury.events.TotalDistribution, event_schema=TotalDistributionEventSchema
        ),
    ]
    event_scanners = [EventScanner(event_handler) for event_handler in event_handlers]
    await asyncio.gather(*[scanner.start() for scanner in event_scanners])


if __name__ == "__main__":
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.create_task(run_event_scanners())
    loop.run_forever()
