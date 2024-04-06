from .settings import Settings, BASE_DIR
from .config import Config
from .log import configure_logging

configure_logging()
settings = Settings()
config = Config()
