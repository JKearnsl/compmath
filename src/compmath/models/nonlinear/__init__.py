from compmath.models import MenuItem
from compmath.models.base import BaseModel


class NoNLinearModel(BaseModel):
    """
    Решение нелинейных уравнений
    Лабораторная работа №2

    """

    id: MenuItem = MenuItem.NONLINEAR

    def __init__(self):
        super().__init__()
