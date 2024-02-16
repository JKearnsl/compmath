from abc import abstractmethod
from dataclasses import dataclass

from compmath.models.base import BaseModel
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable, FunctionValidateError


@dataclass
class TableRow:
    iter_num: int
    vector: list[int | float]
    delta: float


class BaseSNEModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._title = "None"
        self._description = "None"
        self._eps = 0.0001
        self.equations: list[str] = []
        self.initial_guess: tuple[int | float, int | float] = (0, 1)
        self._iters_limit = 100
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

    def set_initial_guess(self, value: tuple[int | float, int | float]):
        if not isinstance(value, tuple):
            raise ValueError(f"Неверное начальное приближение {value!r} type {type(value)!r}")

        if len(value) != 2:
            raise ValueError(f"Неверное начальное приближение {value!r} type {type(value)!r}")

        self.initial_guess = value
        self.notify_observers()

    @abstractmethod
    def calc(self) -> None:
        ...

    def was_calculated(self):
        for observer in self._mObservers:
            observer.was_calculated()

    def validation_error(self, error):
        for observer in self._mObservers:
            observer.validation_error(error)

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

    def set_equation_count(self, value: int):
        if not isinstance(value, int):
            raise ValueError(f"Неверное количество уравнений {value!r} type {type(value)!r}")

        if value < 2:
            self.validation_error("Неверное количество уравнений")
            return

        if value > len(self.equations):
            self.equations.extend(["" for _ in range(value - len(self.equations))])
        else:
            self.equations = self.equations[:value]
        self.notify_observers()

    def set_equation(self, index: int, value: str):
        if not isinstance(index, int):
            raise ValueError(f"Неверный индекс уравнения {index!r} type {type(index)!r}")

        if not isinstance(value, str):
            raise ValueError(f"Неверное уравнение {value!r} type {type(value)!r}")

        if index < 0 or index >= len(self.equations):
            raise ValueError("Неверный индекс уравнения")

        try:
            make_callable(value)
        except FunctionValidateError:
            self.validation_error(f"Неверное уравнение {index + 1!r}")
            return

        self.equations[index] = value
        self.notify_observers()
