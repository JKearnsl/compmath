from abc import abstractmethod

from compmath.models.base import BaseModel
from compmath.models.nonlinear.graphic import Graphic
from compmath.utils.func import make_callable, FunctionValidateError


class BaseNoNLinearModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._title = "None"
        self._description = "None"
        self._fx = "None"
        self._interval = (0, 1)
        self._eps = 0
        self.result = None
        self.iters = None
        self._y_limits = (-10, 10)
        self._x_limits = (-10, 10)
        self.graphics: list[Graphic] = []

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
            make_callable(fx)
        except FunctionValidateError as error:
            self.validation_error("Инвалидная функция")
            return

        self._fx = fx
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

        if eps <= 0:
            self.validation_error("Неверная точность")
            return

        self._eps = eps
        self.notify_observers()

    @property
    def y_limits(self) -> tuple[float | int, float | int]:
        return self._y_limits

    @property
    def x_limits(self) -> tuple[float | int, float | int]:
        return self._x_limits

    def set_y_limits(self, y_limits: tuple[float | int, float | int]):
        if not isinstance(y_limits, tuple):
            raise ValueError("Неверно задан предел по Y")

        if len(y_limits) != 2:
            raise ValueError("Неверно задан предел по Y")

        if not isinstance(y_limits[0], (int, float)) or not isinstance(y_limits[1], (int, float)):
            raise ValueError("Неверно задан предел по Y")

        if y_limits[0] >= y_limits[1]:
            self.validation_error("Неверно задан предел по Y")
            return

        self._y_limits = y_limits
        self.notify_observers()
        # self.calc()

    def set_x_limits(self, x_limits: tuple[float | int, float | int]):
        if not isinstance(x_limits, tuple):
            raise ValueError("Неверно задан предел по X")

        if len(x_limits) != 2:
            raise ValueError("Неверно задан предел по X")

        if not isinstance(x_limits[0], (int, float)) or not isinstance(x_limits[1], (int, float)):
            raise ValueError("Неверно задан предел по X")

        if x_limits[0] >= x_limits[1]:
            self.validation_error("Неверно задан предел по X")
            return

        self._x_limits = x_limits
        self.notify_observers()

    @abstractmethod
    def calc(self) -> None:
        ...

    def derivative(self, fx: str, x: float) -> float:
        """
        Производная функции

        :param fx:
        :param x:
        :return:
        """
        raise NotImplementedError

    def validation_error(self, error):
        for observer in self._mObservers:
            observer.validation_error(error)
