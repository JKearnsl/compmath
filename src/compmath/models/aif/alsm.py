from typing import cast, Callable

import numpy as np

from compmath.models.aif.base import BaseAIFModel
from compmath.models.graphic import Graphic
from compmath.utils.func import linfit, expfit, lgsfit, sinfit, pwrfit


class ALSModel(BaseAIFModel):
    """
    Аппроксимация: Метод наименьших квадратов

    """

    def __init__(self):
        super().__init__()
        self._title = "Аппроксимация: Метод наименьших квадратов"
        self._description = """
            Включает в себя методы линейной регрессии, полиномиальной регрессии, 
            линейной комбинации линейно-независимых функций, нелинейной зависимости от параметра.
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
        self.results.clear()
        points = sorted(self.points, key=lambda _: _[0])

        self.results.append(self.linear_regression(points))
        self.results.append(self.polynomial_regression(points, 2))
        self.results.append(self.polynomial_regression(points, 3))
        self.results.append(self.lclif(points))
        self.results.append(self.ndp(points, expfit))
        self.results.append(self.ndp(points, lgsfit))
        self.results.append(self.ndp(points, sinfit))
        self.results.append(self.ndp(points, pwrfit))

        self.notify_observers()

    def linear_regression(
            self, points: list[tuple[float, float]]
    ) -> tuple[Graphic, list[str], tuple[float, float], str]:
        """
        Линейная регрессия

        :param points: отсортированный двумерный массив точек (x, y)
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
        log = []

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

        log.append(f"\nУравнение регрессии: \nf(x) = {a0} + {a1} * x\n")

        # Сумма квадратов разностей:
        sum_diff = sum([(y[i] - func(x[i])) ** 2 for i in range(n)])
        log.append(f"Сумма квадратов разностей: {sum_diff}")

        for point in points:
            graphic.add_point(point[0], point[1])
        graphic.add_graph(func)

        return graphic, log, (sum_diff, r), "Линейная регрессия"

    def polynomial_regression(
            self, points: list[tuple[float, float]], degree: int
    ) -> tuple[Graphic, list[str], tuple[float, float], str]:
        """
        Полиномиальная регрессия n-ой степени

        :param points: отсортированный двумерный массив точек (x, y)
        :param degree: степень полинома
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
        log = []

        # Коэффициент корреляции
        n = len(points)
        x = [point[0] for point in points]
        y = [point[1] for point in points]

        coefficients = np.polyfit(x, y, degree)
        log.append(f"Коэффициенты полинома: \n{'\n'.join([str(coefficients[i]) for i in range(degree + 1)])}")
        polynomial = np.polynomial.Polynomial(np.flip(coefficients))
        log.append(f"\nУравнение регрессии: f(x) = {polynomial}\n")

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

        for point in points:
            graphic.add_point(point[0], point[1])
        graphic.add_graph(cast(Callable[[float], float], polynomial))

        return graphic, log, (sum_diff, gamma), f"Полиномиальная регрессия {degree}-степени"

    def lclif(self, points: list[tuple[float, float]]) -> tuple[Graphic, list[str], tuple[float, float], str]:
        """
        Линейная комбинация линейно-независимых функций

        :param points: отсортированный двумерный массив точек (x, y)
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
        log = []

        x = [point[0] for point in points]
        y = [point[1] for point in points]

        def f(t): return 1, t, t ** 3, t ** 5, t ** 7

        k = linfit(x, y, f)
        log.append(f"Коэффициенты линейной комбинации: K = \n{'\n'.join([str(_) for _ in k])}\n")

        def k1(t): return np.dot(k, f(t))

        log.append(f"\nУравнение регрессии: k1(t) = k * f(t)\n")

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

        for point in points:
            graphic.add_point(point[0], point[1])
        graphic.add_graph(k1)

        return graphic, log, (sum_diff, gamma), "Линейная комбинация линейно-независимых функций"

    def ndp(
            self,
            points: list[tuple[float, float]],
            fit: Callable[[list[float], list[float], list[float | int] | None], tuple] = expfit
    ) -> tuple[Graphic, list[str], tuple[float, float], str]:
        """
        Нелинейная зависимость от параметра

        :param fit: функция регрессии
        :param points:
        :return:
        """

        graphic = Graphic(self._x_limits, self._y_limits)
        log = []

        x = [point[0] for point in points]
        y = [point[1] for point in points]

        g = [1, 1, 0]
        q = fit(x, y, g)
        log.append(f"Коэффициенты нелинейной зависимости от параметра: q = \n{'\n'.join([str(_) for _ in q[0]])}\n")

        def func(t): return q[1](t)

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

        for point in points:
            graphic.add_point(point[0], point[1])
        graphic.add_graph(func)

        return graphic, log, (sum_diff, gamma), f"Нелинейная зависимость от параметра (метод {fit.__name__})"
