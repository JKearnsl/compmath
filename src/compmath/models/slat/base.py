from abc import abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import Sequence

import numpy as np
import sympy as sp

from compmath.models.base import BaseModel


@dataclass
class TableRow:
    iter_num: int
    vector: list[int | float]
    delta: float


class BaseSLATModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._title = "None"
        self._description = "None"
        self._eps = 0.0001
        self.matrix: list[list[int | float]] = [
            [1.53, -1.65, -0.76, 2.18],
            [0.86, 1.17, 1.84, 1.95],
            [0.32, -0.65, 1.11, -0.47]
        ]
        self.x0: list[int | float] = []
        self._iters_limit = 100
        self.results: list[tuple[list[str], list[TableRow], str]] = []

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

    def normal_matrix(self) -> tuple[np.ndarray[float], np.ndarray[float]]:
        new_matrix = np.array(deepcopy(self.a()), dtype=float)
        a_matrix = np.dot(new_matrix.T, new_matrix)
        b_matrix = np.dot(new_matrix.T, self.b())
        return a_matrix, b_matrix

    def transform_matrix(self) -> tuple[Sequence[Sequence[float]], Sequence[float], list[str]]:
        a_matrix = deepcopy(self.a())
        b_vector = deepcopy(self.b())

        n = len(a_matrix)
        # Создание символьных матриц для работы с элементарными преобразованиями
        a_sym = sp.Matrix(a_matrix)
        b_sym = sp.Matrix(b_vector)
        transformations_log = []  # Лог для записи действий

        for i in range(n):
            # Поиск максимального элемента в столбце i
            max_index = i
            for j in range(i + 1, n):
                if abs(a_sym[j, i]) > abs(a_sym[max_index, i]):
                    max_index = j
            if max_index != i:
                # Перестановка строк для диагонального преобладания
                a_sym.row_swap(i, max_index)
                b_sym.row_swap(i, max_index)
                transformations_log.append(f"Перестановка строк: {i + 1} и {max_index + 1}")

            # Выполнение диагонального преобразования
            pivot = a_sym[i, i]
            for j in range(i + 1, n):
                if pivot == 0:
                    break  # Пропустить, если главный элемент равен нулю
                ratio = a_sym[j, i] / pivot
                a_sym.row_op(j, lambda x, k: x - ratio * a_sym[i, k])
                b_sym.row_op(j, lambda x, k: x - ratio * b_sym[i, k])
                transformations_log.append(f"Вычитание из строки {j + 1} строки {i + 1}, умноженной на {ratio}")

        # Возвращение результатов преобразований и лога
        return a_sym.tolist(), [el[0] for el in b_sym.tolist()], transformations_log
