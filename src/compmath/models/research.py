from compmath.models import MenuItem
from compmath.models.base import BaseModel


class ResearchModel(BaseModel):
    """
    Исследование функций
    Лабораторная работа №1

    """

    id: MenuItem = MenuItem.RESEARCH

    def __init__(self):
        super().__init__()
