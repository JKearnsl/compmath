from abc import abstractmethod
from dataclasses import dataclass

from compmath.models.base import BaseGraphicModel
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable, FunctionValidateError


@dataclass
class TableRow:
    iter_num: int
    x: float
    fx: float
    a: float | None
    fa: float | None
    b: float | None
    fb: float | None
    distance: float | None


class BaseNoNLinearModel(BaseGraphicModel):

    def __init__(self):
        super().__init__()
        self._title = "None"
        self._description = "None"
        self._fx = "None"
        self._interval = (0, 1)
        self._eps = 0
        self._iters_limit = 100
        self.result = None
        self.iters = None
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
    def fx(self) -> str:
        return self._fx

    def set_fx(self, fx: str):
        try:
            func = make_callable(fx)
        except FunctionValidateError:
            self.validation_error("Инвалидная функция")
            return

        self._fx = fx
        self.graphics.clear()
        graphic = Graphic(x_limits=self._x_limits, y_limits=self._y_limits)
        graphic.add_graph(func)
        self.graphics.append(graphic)
        self.notify_observers()

    def reset_graphic(self):
        self.graphics.clear()
        graphic = Graphic(x_limits=self._x_limits, y_limits=self._y_limits)

        try:
            func = make_callable(self.fx)
        except FunctionValidateError:
            func = None

        if func:
            graphic.add_graph(func)
            self.graphics.append(graphic)
        self.notify_observers()

    @property
    def interval(self) -> tuple[float | int, float | int]:
        return self._interval

    def set_interval(self, interval: tuple[float | int, float | int]):
        if not isinstance(interval, tuple):
            raise ValueError("Неверный интервал")

        if len(interval) != 2:
            raise ValueError("Неверный интервал")

        if not isinstance(interval[0], (int, float)) or not isinstance(interval[1], (int, float)):
            raise ValueError("Неверный интервал")

        if interval[0] >= interval[1]:
            self.validation_error("Неверный интервал")
            return

        self._interval = interval
        self.notify_observers()

    @property
    def eps(self) -> float:
        return self._eps

    def set_eps(self, eps: float):
        if not isinstance(eps, (int, float)):
            raise ValueError(f"Неверная точность {eps!r} type {type(eps)!r}")

        if eps <= 0 or eps >= 1:
            self.validation_error("Неверная точность")
            return

        self._eps = eps
        self.notify_observers()

    @property
    def iters_limit(self) -> int:
        return self._iters_limit

    def set_iters_limit(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError(f"Неверный параметр max_iters {value!r} type {type(value)!r}")

        if value <= 0:
            self.validation_error("Неверный параметр ограничения итераций")
            return

        self._iters_limit = value
        self.notify_observers()

    @abstractmethod
    def calc(self) -> None:
        ...
