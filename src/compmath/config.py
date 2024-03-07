import os
from dataclasses import dataclass
import configparser
from uuid import UUID

from compmath.version import __version__


@dataclass
class Contact:
    NAME: str | None
    URL: str | None
    EMAIL: str | None


@dataclass
class Base:
    APP_NAME: str
    DEBUG: bool
    THEME_UUID: UUID
    CONTACT: Contact


@dataclass
class CalcServer:
    HOST: str
    PORT: int


@dataclass
class Config:
    VERSION: str
    BASE: Base
    CALC_SERVER: CalcServer


def str_to_bool(value: str) -> bool:
    return value.lower() in ("yes", "true", "t", "1")


class InIConfig:
    VAR: Config
    raw: configparser.ConfigParser

    def __init__(self, path: str | os.PathLike, encoding="utf-8"):
        config = configparser.ConfigParser()
        config.read(filenames=path, encoding=encoding)

        self.VAR = Config(
            VERSION=__version__,
            BASE=Base(
                APP_NAME=config["BASE"]["APP_NAME"],
                DEBUG=str_to_bool(config["BASE"]["DEBUG"]),
                THEME_UUID=UUID(config["BASE"]["THEME_UUID"]),
                CONTACT=Contact(
                    NAME=config["CONTACT"]["NAME"],
                    URL=config["CONTACT"]["URL"],
                    EMAIL=config["CONTACT"]["EMAIL"]
                ),
            ),
            CALC_SERVER=CalcServer(
                HOST=config["CALC_SERVER"]["HOST"],
                PORT=int(config["CALC_SERVER"]["PORT"])
            )
        )
        self.path = path
        self.raw = config

    def reload(self):
        self.__init__(self.path)

    def save(self):
        with open(self.path, "w") as file:
            self.raw.write(file)
