from compmath.models import MenuItem
from compmath.models.base import BaseModel


class SLATModel(BaseModel):
    """
    Системы линейных алгебраических уравнений
    Лабораторная работа №3

    """

    id: MenuItem = MenuItem.SLAT

    def __init__(self):
        super().__init__()
