from typing import cast

import numpy as np

from compmath.models.graphic import Graphic
from compmath.models.sne.base import BaseSNEModel, TableRow
from compmath.utils.func import make_callable, solve_rel_var


class ZModel(BaseSNEModel):

    def __init__(self):
        super().__init__()

        self._title = "Метод Зейделя"
        self._description = "Метод Зейделя - модификация метода простых итераций..."

    def calc(self):
        self.table.clear()
        self.solve_log.clear()
        self.graphics.clear()

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

        fi_x_y = (
            make_callable(solve_rel_var(func_str_1, "x")[0]),
            make_callable(solve_rel_var(func_str_2, "y")[0])
        )

        x_vector = np.array([0, 0], dtype=float)

        k = 0
        delta = 2 * self.eps
        while delta > self.eps and k < self._iters_limit:
            k += 1

            x0 = x_vector.copy()

            for i in range(len(x_vector)):
                x_vector[i] = fi_x_y[i](*x_vector)

            delta = np.max(np.abs(x_vector - x0))

            self.table.append(TableRow(k, list(x_vector), delta))
            graphic = Graphic(x_limits=self.x_limits, y_limits=self.x_limits)
            graphic.add_graph(fx=fi_x_y[0], color="blue")
            graphic.add_graph(fy=fi_x_y[1], color="red")
            graphic.add_point(
                cast(float, x_vector[1]),
                cast(float, x_vector[0]),
                color="green"
            )
            self.graphics.append(graphic)

        self.solve_log.append(f"\nРешение: {x_vector}")
        self.notify_observers()
