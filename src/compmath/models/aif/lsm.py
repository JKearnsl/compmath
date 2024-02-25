from typing import cast, Callable

import numpy as np

from compmath.models.aif.base import BaseAIFModel
from compmath.models.graphic import Graphic


class LSModel(BaseAIFModel):
    """
    Метод наименьших квадратов

    """

    def __init__(self):
        super().__init__()
        self._title = "Метод наименьших квадратов"
        self._description = """
            ...
        """
        self._points = [
            (-4.38, 2.25),
            (-3.84, 2.83),
            (-3.23, 3.44),
            (-2.76, 4.31),
            (-2.22, 5.29),
            (-1.67, 6.55),
            (-1.13, 8.01),
            (-0.60, 10.04)
        ]

    def calc(self) -> None:
        points = sorted(self.points, key=lambda _: _[0])

        graphic, log = self.linear_regression(points)

        self.notify_observers()

    def linear_regression(self, points: list[tuple[float, float]]) -> tuple[Graphic, list[str]]:
        """
        Линейная регрессия

        :param points: отсортированный двумерный массив точек (x, y)
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
        log = ["\nЛинейная регрессия:\n"]

        # Коэффициент корреляции
        n = len(points)
        x = [point[0] for point in points]
        y = [point[1] for point in points]
        sum_x = sum(x)
        sum_y = sum(y)
        sum_x2 = sum([i ** 2 for i in x])
        sum_y2 = sum([i ** 2 for i in y])
        sum_xy = sum([x[i] * y[i] for i in range(n)])
        r = (n * sum_xy - sum_x * sum_y) / ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
        log.append(f"Коэффициент корреляции: {r}")

        # Линейная регрессия
        a1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        a0 = (sum_y - a1 * sum_x) / n

        def func(arg): return a0 + a1 * arg

        log.append(f"Уравнение регрессии: f(x) = {a0} + {a1} * x")

        # Сумма квадратов разностей:
        sum_diff = sum([(y[i] - func(x[i])) ** 2 for i in range(n)])
        log.append(f"Сумма квадратов разностей: {sum_diff}")

        for point in points:
            graphic.add_point(point[0], point[1])
        graphic.add_graph(func)

        return graphic, log
