from sympy import diff
import numpy as np

from compmath.models.sne.base import BaseSNEModel, TableRow
from compmath.utils.func import solve_rel_var, make_callable


class NTModel(BaseSNEModel):

    def __init__(self):
        super().__init__()

        self._title = "Метод Ньютона"
        self._description = "..."

    def calc(self):
        self.table.clear()
        self.solve_log.clear()

        if len(self.equations) != 2:
            self.validation_error("Должно быть два уравнения")
            return

        func_str_1 = self.equations[0]
        func_str_2 = self.equations[1]

        self.solve_log.append(f"Уравнение 1: {func_str_1}")
        self.solve_log.append(f"Уравнение 2: {func_str_2}")

        # Проверка итерационной сходимости

        if not self.is_converges(func_str_1, func_str_2):
            self.notify_observers()
            self.validation_error("Не выполнено условие сходимости")
            return

        # Решение

        # Матрица Якоби
        w = [
            [diff(func_str_1, "x"), diff(func_str_1, "y")],
            [diff(func_str_2, "x"), diff(func_str_2, "y")]
        ]
        x_vector = np.array(self.initial_guess, dtype=float)

        self.solve_log.append(f"W(x, y) = {w}")

        for i, row in enumerate(w):
            for j, el in enumerate(row):
                w[i][j] = make_callable(el)

        k = 0
        delta = 2 * self.eps
        while delta > self.eps and k < self._iters_limit:
            k += 1

            # Вектор поправок delta_x_vector = - W(x_vector_1, x_vector_2)^-1 * F(x_vector_1, x_vector_2)
            w_matrix = np.array([
                [w[0][0](*x_vector), w[0][1](*x_vector)],
                [w[1][0](*x_vector), w[1][1](*x_vector)]
            ])

            delta_x = -np.dot(np.linalg.inv(w_matrix), [
                make_callable(func_str_1)(*x_vector),
                make_callable(func_str_2)(*x_vector)
            ])

            # Уточнение решения
            x_vector = delta_x + x_vector

            # Расчет оценки достаточной точности
            delta = np.max(np.abs(delta_x))

            self.table.append(TableRow(k, x_vector, delta))

        self.solve_log.append(f"\nРешение: {x_vector}")
        self.notify_observers()
