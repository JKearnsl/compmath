from abc import abstractmethod
from dataclasses import dataclass

from compmath.models.base import BaseGraphicModel


@dataclass
class TableRow:
    iter_num: int
    x: float
    fx: float
    distance: float | None


class BaseAIFModel(BaseGraphicModel):

    def __init__(self):
        super().__init__()
        self._title = "None"
        self._description = "None"
        self._points: list[tuple[float, float]] = []
        self.table: list[TableRow] = []

    @property
    def title(self) -> str:
        return self._title

    def set_title(self, title: str):
        self._title = title
        self.notify_observers()

    @property
    def description(self) -> str:
        return self._description

    def set_description(self, description: str):
        self._description = description
        self.notify_observers()

    @property
    def points(self) -> list[tuple[float, float]]:
        return self._points

    def resize(self, size: int):
        if len(self._points) < size:
            self._points.extend([(0, 0) for _ in range(size - len(self._points))])
        elif len(self._points) > size:
            self._points = self._points[:size]
        self.notify_observers()

    def set_point(self, pos: int, point: tuple[float, float]):
        if not isinstance(point, tuple):
            raise ValueError("Точка не является кортежем")

        if len(point) != 2:
            raise ValueError("Длина кортежа не равна 2")

        if not isinstance(point[0], (int, float)) or not isinstance(point[1], (int, float)):
            raise ValueError("Точка не является парой чисел")

        self._points[pos] = point
        self.notify_observers()

    @abstractmethod
    def calc(self) -> None:
        ...
