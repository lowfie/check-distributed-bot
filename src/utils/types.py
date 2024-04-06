from typing import Any

from pydantic_core import core_schema
from eth_utils.address import is_address, to_checksum_address
from pydantic import GetCoreSchemaHandler, ValidationInfo


class ChecksumAddress(str):
    """Ethereum address validation"""

    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value

    @classmethod
    def validate(cls, value: str, info: ValidationInfo):
        if not isinstance(value, str):
            raise TypeError("String required")

        if not is_address(value):
            raise ValueError("Not Ethereum address")

        return cls(to_checksum_address(value))

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.validate, handler(str)
        )
