from enum import Enum

import psutil

from compmath.models.base import BaseModel


class MenuItem(str, Enum):
    RESEARCH: str = "RESEARCH"
    NONLINEAR: str = "NONLINEAR"
    SLAT: str = "SLAT"
    SNE: str = "SNE"
    NI: str = "NI"
    AIF: str = "AIF"


class MainModel(BaseModel):

    def __init__(self, **scope):
        super().__init__()
        self.is_debug = scope["is_debug"]
        self.app_title = scope["app_title"]
        self.app_version = scope["app_version"]
        self.contact = scope["contact"]
        self.scope = scope

    @staticmethod
    def get_ram_usage() -> int:
        return int(psutil.Process().memory_info().rss / (1024 * 1024))
