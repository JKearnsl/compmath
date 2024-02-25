from typing import cast, Callable

import numpy as np

from compmath.models.aif.base import BaseAIFModel
from compmath.models.graphic import Graphic
from compmath.utils.func import linfit, expfit


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

        self.results.append(self.linear_regression(points))
        self.results.append(self.polynomial_regression(points, 2))
        self.results.append(self.polynomial_regression(points, 3))
        self.results.append(self.lclif(points))
        self.ndp(points)

        self.notify_observers()

    def linear_regression(self, points: list[tuple[float, float]]) -> tuple[Graphic, list[str], tuple[float, float]]:
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
        log.append(f"Коэффициент корреляции: r = {r}")

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

        return graphic, log, (sum_diff, r)

    def polynomial_regression(
            self, points: list[tuple[float, float]], n: int
    ) -> tuple[Graphic, list[str], tuple[float, float]]:
        """
        Полиномиальная регрессия n-ой степени

        :param points: отсортированный двумерный массив точек (x, y)
        :param n: степень полинома
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
        log = [f"\nПолиномиальная регрессия {n}-степени:\n"]

        # Коэффициент корреляции
        n = len(points)
        x = [point[0] for point in points]
        y = [point[1] for point in points]

        coefficients = np.polyfit(x, y, n)
        log.append(f"Коэффициенты полинома: {coefficients}")
        polynomial = np.poly1d(coefficients)
        log.append(f"Уравнение регрессии: f(x) = {polynomial}")

        # Индекс корреляции
        gamma = np.sqrt(
            1 -
            sum([(y[i] - polynomial(x[i])) ** 2 for i in range(n)]) /
            sum([(y[i] - sum(y) / n) ** 2 for i in range(n)])
        )
        log.append(f"Индекс корреляции: γ = {gamma}")

        # Сумма квадратов разностей:
        sum_diff = sum([(y[i] - polynomial(x[i])) ** 2 for i in range(n)])
        log.append(f"Сумма квадратов разностей: {sum_diff}")

        graphic.add_graph(cast(Callable[[float], float], polynomial))

        return graphic, log, (sum_diff, gamma)

    def lclif(self, points: list[tuple[float, float]]) -> tuple[Graphic, list[str], tuple[float, float]]:
        """
        Линейная комбинация линейно-независимых функций

        :param points: отсортированный двумерный массив точек (x, y)
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
        log = ["\nЛинейная комбинация линейно-независимых функций:\n"]

        x = [point[0] for point in points]
        y = [point[1] for point in points]

        def f(t): return 1, t, t ** 3, t ** 5, t ** 7

        k = linfit(x, y, f)
        log.append(f"Коэффициенты линейной комбинации: K = {k}")

        def k1(t): return np.dot(k, f(t))

        # Сумма квадратов разностей:
        sum_diff = sum([(y[i] - k1(x[i])) ** 2 for i in range(len(points))])
        log.append(f"Сумма квадратов разностей: {sum_diff}")

        # Индекс корреляции
        n = len(points)
        gamma = np.sqrt(
            1 -
            sum([(y[i] - k1(x[i])) ** 2 for i in range(n)]) /
            sum([(y[i] - sum(y) / n) ** 2 for i in range(n)])
        )
        log.append(f"Индекс корреляции: γ = {gamma}")

        graphic.add_graph(k1)

        return graphic, log, (sum_diff, gamma)

    def ndp(
            self,
            points: list[tuple[float, float]],
            fit: Callable[[list[float], list[float], list[float | int] | None], tuple] = expfit
    ) -> tuple[Graphic, list[str], tuple[float, float]]:
        """
        Нелинейная зависимость от параметра

        :param fit: функция регрессии
        :param points:
        :return:
        """

        graphic = Graphic(self._x_limits, self._y_limits)
        log = [f"\nНелинейная зависимость от параметра (метод {fit.__name__}):\n"]

        x = [point[0] for point in points]
        y = [point[1] for point in points]

        g = [1, 1, 0]
        q = fit(x, y, g)
        log.append(f"Коэффициенты нелинейной зависимости от параметра: q = {q}")

        def func(t): return q[0] * np.exp(q[1] * t) + q[2]

        # Сумма квадратов разностей:
        sum_diff = sum([(y[i] - func(x[i])) ** 2 for i in range(len(points))])
        log.append(f"Сумма квадратов разностей: {sum_diff}")

        # Индекс корреляции
        n = len(points)
        gamma = np.sqrt(
            1 -
            sum([(y[i] - func(x[i])) ** 2 for i in range(n)]) /
            sum([(y[i] - sum(y) / n) ** 2 for i in range(n)])
        )
        log.append(f"Индекс корреляции: γ = {gamma}")

        graphic.add_graph(func)

        return graphic, log, (sum_diff, gamma)
