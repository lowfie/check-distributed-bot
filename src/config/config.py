import os
from typing import Any, Type
from functools import partial
from typing_extensions import Self

import yaml
from web3.net import AsyncNet
from web3.eth import AsyncEth
from src.config.settings import BASE_DIR
from pydantic import Field, model_validator
from web3 import AsyncHTTPProvider, AsyncWeb3
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from src.config.abi import aix_treasury
from src.utils.types import ChecksumAddress

DEFAULT_PATH = str(BASE_DIR) + "/src/config/files/dev.yaml"


def _yaml_config_settings_resource_source(path: str | None) -> dict[str, Any]:
    if not path or not os.path.exists(path):
        return dict()
    with open(path) as file:
        config = yaml.safe_load(file)
    return config


class AbiConfig(BaseSettings):
    aix_treasury: list[Any] = aix_treasury


class ContractConfig(BaseSettings):
    aix_treasury: ChecksumAddress


class Web3Config(BaseSettings):
    provider_url: str

    w3: AsyncWeb3 | None = Field(default=None)

    @model_validator(mode="after")
    def set_w3(self) -> Self:
        self.w3 = AsyncWeb3(
            provider=AsyncHTTPProvider(self.provider_url),
            modules={
                "eth": (AsyncEth,),
                "net": (AsyncNet,),
            },
            middlewares=[],
        )
        return self


class ScannerConfig(BaseSettings):
    maximum_scanning_blocks: int
    confirmation_blocks: int
    speedy_polling_interval: int
    polling_interval: int


class BotConfig(BaseSettings):
    token: str
    send_chat_id: str


class Config(BaseSettings):
    bot: BotConfig
    scanner: ScannerConfig
    web3: Web3Config
    contracts: ContractConfig

    abi: AbiConfig = AbiConfig()

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (
            env_settings,
            partial(_yaml_config_settings_resource_source, path=DEFAULT_PATH),
            init_settings,
            file_secret_settings
        )
