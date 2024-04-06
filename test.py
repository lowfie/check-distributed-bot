import asyncio
import datetime

from src.config import config
from src.services import total_distribution
from src.services.total_distribution import TotalDistributedInitial
from src.database.actions import db_session

import datetime


def format_timedelta(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h{int(minutes)}m"


async def main():
    async with db_session() as db:
        distr = "0x9A0A9594Aa626EE911207DC001f535c9eb590b34"

        # Получение баланса кошелька в wei
        balance_wei = await config.web3.w3.eth.get_balance(distr)

        # Конвертация баланса из wei в ether
        balance_eth = config.web3.w3.from_wei(balance_wei, 'ether')

        print("Баланс кошелька:", balance_eth, "ETH")


if __name__ == '__main__':
    asyncio.run(main())
