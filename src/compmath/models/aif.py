from compmath.models import MenuItem
from compmath.models.base import BaseModel


class AIFModel(BaseModel):
    """
    Аппроксимация и интерполяция функций
    Лабораторная работа №6
    """

    id: MenuItem = MenuItem.AIF

    def __init__(self):
        super().__init__()


