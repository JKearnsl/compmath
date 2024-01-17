from compmath.models import MenuItem
from compmath.models.base import BaseModel


class SNEModel(BaseModel):
    """
    Численные методы решения систем нелинейных уравнений.
    Лабораторная работа №4

    """

    id: MenuItem = MenuItem.SNE

    def __init__(self):
        super().__init__()
