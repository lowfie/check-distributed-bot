from src.config import config
from src.services.bot import bot
from src.database.actions import db_session
from src.services import total_distribution
from src.utils.helpers import format_timedelta
from src.services.worker.tasks import AsyncTask
from src.services.total_distribution import TotalDistributedInitial


class SendDistributedStatisticTask(AsyncTask):
    async def run_async(self):
        async with db_session() as db:
            (
                total_input_aix,
                total_distributed_aix,
                total_swapped_eth,
                total_distributed_eth
            ) = await total_distribution.statistic(
                db=db,
                days=1,
            )

            # TODO: move config or get from contracts
            decimals = 10**18

            aix_processed = round(total_input_aix / decimals, 2) if total_distributed_aix else 0
            aix_distributed = round(total_distributed_aix / decimals, 2) if total_distributed_aix else 0
            eth_bought = round(total_swapped_eth / decimals, 2) if total_swapped_eth else 0
            eth_distributed = round(total_distributed_eth / decimals, 2) if total_distributed_eth else 0

            last_instance = await total_distribution.first_or_last_instance(
                db=db,
                initial=TotalDistributedInitial.LAST
            )
            first_instance = await total_distribution.first_or_last_instance(
                db=db,
                initial=TotalDistributedInitial.FIRST
            )
            last_instance_time = format_timedelta(last_instance.created_at) if last_instance else "0h0m"
            first_instance_time = format_timedelta(first_instance.created_at) if first_instance else "0h0m"

            # TODO: move config
            distributor = "0x9A0A9594Aa626EE911207DC001f535c9eb590b34"

            balance_wei = await config.web3.w3.eth.get_balance(distributor)
            balance_eth = config.web3.w3.from_wei(balance_wei, 'ether')

            message = (
                "<b>Daily $AIX Stats:</b>\n\n"
                f"- First TX: {first_instance_time} ago\n"
                f"- Last TX: {last_instance_time} ago\n"
                f"- AIX processed: {aix_processed}\n"
                f"- AIX distributed: {aix_distributed}\n"
                f"- ETH bought: {eth_bought}\n"
                f"- ETH distributed: {eth_distributed}\n\n"
                f"Distributor wallet: <code>0x9A0A9594Aa626EE911207DC001f535c9eb590b34</code>\n"
                f"Distributor balance: {round(balance_eth, 5)} ETH"
            )

            await bot.send_message(
                chat_id=config.bot.send_chat_id,
                text=message
            )
