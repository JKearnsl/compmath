import os
from dataclasses import dataclass

from compmath_calc_server.version import __version__


@dataclass
class Config:
    DEBUG: bool
    VERSION: str


def str_to_bool(value: str) -> bool:
    return str(value).lower() in ("yes", "true", "t", "1")


def load_config() -> Config:
    return Config(
        DEBUG=str_to_bool(os.environ.get("DEBUG", 1)),
        VERSION=__version__,
    )
