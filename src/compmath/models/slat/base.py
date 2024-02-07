from abc import abstractmethod

from compmath.models.base import BaseModel


class BaseSLATModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._title = "None"
        self._description = "None"
        self._eps = 0.0001
        self.matrix: list[list[int | float]] = []
        self.x0: list[int | float] = []
        self.result: list[tuple[int, ...]] = []
        self._iters_limit = 100
        self.iters = None

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

    def a(self) -> list[list[int | float]]:
        return [row[:-1] for row in self.matrix]

    def b(self) -> list[int | float]:
        return [row[-1] for row in self.matrix]

    def set_eps(self, eps: float):
        if not isinstance(eps, (int, float)):
            raise ValueError(f"Неверная точность {eps!r} type {type(eps)!r}")

        if eps <= 0:
            self.validation_error("Неверная точность")
            return

        self._eps = eps
        self.notify_observers()

    def resize(self, value: int) -> None:
        if self.size() == value or value < 3 or value > 8:
            return

        if len(self.x0) < value:
            for _ in range(len(self.x0), value):
                self.x0.append(0)
        elif len(self.x0) > value:
            self.x0 = self.x0[:value]

        if not self.matrix:
            for i in range(value):
                self.matrix.append([0 for _ in range(value + 1)])
            self.notify_observers()
            return

        delta = abs(len(self.matrix) - value)
        if len(self.matrix) < value:
            for i in range(len(self.matrix), value):
                self.matrix.append([0 for _ in range(len(self.matrix[0]))])

            for row in self.matrix:
                for _ in range(delta):
                    row.insert(-1, 0)
        else:
            self.matrix = self.matrix[:value]
            for row in self.matrix:
                for _ in range(delta):
                    row.pop(-2)

        self.notify_observers()

    def size(self) -> int:
        return len(self.matrix)

    def set_item_value(self, row: int, column: int, value: int | float):
        self.matrix[row][column] = value
        self.notify_observers()

    def set_item_x0_value(self, index: int, value: int | float):
        self.x0[index] = value
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
