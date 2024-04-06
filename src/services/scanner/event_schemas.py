from hexbytes import HexBytes
from pydantic import BaseModel

from pydantic_settings import SettingsConfigDict

from src.utils.helpers import to_lower_camel
from src.utils.types import ChecksumAddress


class EventBaseSchema(BaseModel):
    model_config = SettingsConfigDict(alias_generator=to_lower_camel)

    args: dict
    event: str
    log_index: int
    transaction_index: int
    transaction_hash: bytes
    address: ChecksumAddress
    block_hash: bytes
    block_number: int


class TotalDistributionEventSchema(EventBaseSchema):
    class TotalDistributionArgs(BaseModel):
        model_config = SettingsConfigDict(alias_generator=to_lower_camel)

        input_aix_amount: int
        distributed_aix_amount: int
        swapped_eth_amount: int
        distributed_eth_amount: int

    args: TotalDistributionArgs
