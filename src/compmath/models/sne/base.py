from abc import abstractmethod
from dataclasses import dataclass

from sympy import diff

from compmath.models.base import BaseGraphicModel
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable, solve_rel_var, is_valid_func


@dataclass
class TableRow:
    iter_num: int
    vector: list[int | float]
    delta: float


class BaseSNEModel(BaseGraphicModel):

    def __init__(self):
        super().__init__()
        self._title = "None"
        self._description = "None"
        self._eps = 0.00001
        self.equations: list[str] = [
            "x + cos(y) - 3",
            "cos(x - 1) - y - 1.2"
        ]
        self.initial_guess: tuple[int | float, int | float] = (0, 1)
        self.solve_log: list[str] = []
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

        if not is_valid_func(value, ["x", "y"]):
            self.validation_error(f"Неверное выражение {value!r}")
            return

        self.equations[index] = value
        self.notify_observers()

    def graphic(self) -> Graphic:
        graphic = Graphic(x_limits=self._x_limits, y_limits=self._y_limits)

        iterable = zip(
            filter(lambda f: f != "", self.equations),
            [
                ("x", "blue"),
                ("y", "red")
            ],
            strict=False
        )
        for func_str, var in iterable:
            solutions = solve_rel_var(func_str, var[0])

            if len(solutions) == 0:
                continue
            if var[0] == "x":
                graphic.add_graph(fx=make_callable(solutions[0]), color=var[1])
            else:
                graphic.add_graph(fy=make_callable(solutions[0]), color=var[1])
        return graphic

    def is_converges(self, func1: str, func2: str) -> bool:
        self.solve_log.append("\nПроверка итерационной сходимости\n")

        fi_x_y = (
            solve_rel_var(func1, "x")[0],
            solve_rel_var(func2, "y")[0]
        )

        fi_1_x_y = (
            diff(fi_x_y[0], "x"),
            diff(fi_x_y[0], "y")
        )

        fi_2_x_y = (
            diff(fi_x_y[1], "x"),
            diff(fi_x_y[1], "y")
        )

        a, b = self.initial_guess

        one = abs(make_callable(fi_1_x_y[0])(a, b)) + abs(make_callable(fi_1_x_y[1])(a, b))
        two = abs(make_callable(fi_2_x_y[0])(a, b)) + abs(make_callable(fi_2_x_y[1])(a, b))

        self.solve_log.append(f"fi(x, y) = {fi_x_y}")
        self.solve_log.append(f"fi₁'(x, y) = {fi_1_x_y}")
        self.solve_log.append(f"fi₂'(x, y) = {fi_2_x_y}")
        self.solve_log.append(f"\na = {a}\nb = {b}\n")
        self.solve_log.append(f"abs(fi₁.₁'(a, b)) + abs(fi₁.₂'(a, b)) = {one} {'<' if one < 1 else '>'} 1")
        self.solve_log.append(f"abs(fi₂.₁'(a, b)) + abs(fi₂.₂'(a, b)) = {two} {'<' if two < 1 else '>'} 1")

        if not (result := one < 1 and two < 1):
            self.solve_log.append("\nУсловие сходимости не выполнено\n")
        else:
            self.solve_log.append("\nУсловие сходимости выполнено\n")
        return result
