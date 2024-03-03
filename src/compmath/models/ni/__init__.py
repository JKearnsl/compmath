from compmath.models import MenuItem
from compmath.models.base import BaseModel


class NIModel(BaseModel):
    """
    Численное интегрирование
    Лабораторная работа №5

    """

    id: MenuItem = MenuItem.NI

    def __init__(self):
        super().__init__()
