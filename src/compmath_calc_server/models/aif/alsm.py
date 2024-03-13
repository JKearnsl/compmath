from copy import deepcopy
from typing import cast, Callable, Sequence

import numpy as np

from compmath_calc_server.models.graphic import GraphicBuilder, GraphicItem
from compmath_calc_server.models.aif.dto import InputAIFModel, ResultAIFItem
from compmath_calc_server.utils.func import linfit, expfit, lgsfit, sinfit, pwrfit, gauss_calc

type RegressReturn = tuple[list[GraphicItem], list[str], tuple[float, float] | tuple[None, None], str]


def calc(data: InputAIFModel) -> list[ResultAIFItem]:
    results = []

    points = sorted(data.points, key=lambda _: _[0])

    results.append(linear_regression(points, data.x_limits, data.y_limits))

    x_vector, y_vector = zip(*points)
    matrix_a = cast(list[list], [[None for _ in range(4)] for _ in range(4)])
    for i, row in enumerate(matrix_a):
        for j, col in enumerate(row):
            matrix_a[i][j] = sum(x ** (i + j) for x in x_vector)

    b_vector = cast(list[float], [None for _ in range(4)])
    for i in range(len(b_vector)):
        b_vector[i] = sum(y * x ** i for x, y in zip(x_vector, y_vector))

    results.append(polynomial_regression(points, 2, matrix_a, b_vector, data.x_limits, data.y_limits))
    results.append(polynomial_regression(points, 3, matrix_a, b_vector, data.x_limits, data.y_limits))
    results.append(polynomial_regression(points, 4, matrix_a, b_vector, data.x_limits, data.y_limits))
    results.append(lclif(points, data.x_limits, data.y_limits))

    results.append(ndp(points, expfit, data.x_limits, data.y_limits))
    results.append(ndp(points, lgsfit, data.x_limits, data.y_limits))
    results.append(ndp(points, sinfit, data.x_limits, data.y_limits))
    results.append(ndp(points, pwrfit, data.x_limits, data.y_limits))

    return [
        ResultAIFItem(
            graphic_items=result[0],
            log=result[1],
            sum_diff=result[2][0],
            coefficient=result[2][1],
            title=result[3]
        ) for result in results
    ]


def linear_regression(
        points: list[tuple[float, float]],
        x_limits: tuple[float | int, float | int],
        y_limits: tuple[float | int, float | int]
) -> RegressReturn:
    """
    Линейная регрессия

    :param points: отсортированный двумерный массив точек (x, y)
    :param x_limits:
    :param y_limits:
    :return: график, лог
    """
    graphic = GraphicBuilder(x_limits, y_limits)
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

    return graphic.build(), log, (sum_diff, r), "Линейная регрессия"


def polynomial_regression(
        points: list[tuple[float, float]],
        degree: int,
        a_matrix: list[list],
        b_vector: list,
        x_limits: tuple[float | int, float | int],
        y_limits: tuple[float | int, float | int]
) -> RegressReturn:
    """
    Полиномиальная регрессия n-ой степени

    :param points: отсортированный двумерный массив точек (x, y)
    :param degree: степень полинома
    :param a_matrix
    :param b_vector
    :param x_limits:
    :param y_limits:
    :return: график, лог
    """
    graphic = GraphicBuilder(x_limits, y_limits)
    log = []

    # Коэффициент корреляции
    n = len(points)
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    coefficients = np.polyfit(x, y, degree)
    log.append(f"Коэффициенты полинома: \n{'\n'.join([str(coefficient) for coefficient in coefficients])}")
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

    # Gauss
    gauss_vector = gauss_calc(deepcopy(a_matrix), deepcopy(b_vector), degree)
    log.append(
        f"\nМатрица A: \n{'\n'.join(['\t'.join([str(round(_, 4)) for _ in row]) for row in a_matrix])}"
    )
    log.append(
        f"\nВектор B: \n{'\n'.join([str(round(_, 5)) for _ in b_vector])}"
    )
    log.append(
        f"\nКоэффициенты полинома (метод Гаусса): "
        f"\n{'\n'.join([str(coefficient) for coefficient in gauss_vector[0]])}"
    )
    log.append(
        f"\nВектор невязок: "
        f"\n{'\n'.join([str(round(_, 5)) for _ in gauss_vector[1]])}"
    )

    log.append("\nТреугольная матрица\n")
    t_matrix = cast(Sequence[Sequence[float]], gauss_vector[2])
    for row in t_matrix:
        log.append("\t".join(str(round(cell, 2)) for cell in row))

    return graphic.build(), log, (sum_diff, gamma), f"Полиномиальная регрессия {degree}-степени"


def lclif(
        points: list[tuple[float, float]],
        x_limits: tuple[float | int, float | int],
        y_limits: tuple[float | int, float | int]
) -> RegressReturn:
    """
    Линейная комбинация линейно-независимых функций

    :param points: отсортированный двумерный массив точек (x, y)
    :param x_limits:
    :param y_limits:
    :return: график, лог
    """
    graphic = GraphicBuilder(x_limits, y_limits)
    log = []

    x = [point[0] for point in points]
    y = [point[1] for point in points]

    def f(t): return 1, t, t ** 3, t ** 5, t ** 7
    log.append(f"Функция: f(t) = 1, t, t^3, t^5, t^7\n")

    k = linfit(x, y, f)
    log.append(f"Коэффициенты линейной комбинации (linfit): K = \n{'\n'.join([str(_) for _ in k])}\n")

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

    return graphic.build(), log, (sum_diff, gamma), "Линейная комбинация линейно-независимых функций"


def ndp(
        points: list[tuple[float, float]],
        fit: Callable[[list[float], list[float], list[float | int] | None], tuple],
        x_limits: tuple[float | int, float | int],
        y_limits: tuple[float | int, float | int]
) -> RegressReturn:
    """
    Нелинейная зависимость от параметра

    :param fit: функция регрессии
    :param points:
    :param x_limits:
    :param y_limits:
    :return:
    """

    graphic = GraphicBuilder(x_limits, y_limits)
    log = []

    x = [point[0] for point in points]
    y = [point[1] for point in points]

    g = [1, 1, 0]
    try:
        q = fit(x, y, g)
    except RuntimeError as err:
        log.append(str(err))
        return graphic.build(), log, (None, None), f"Нелинейная зависимость от параметра (метод {fit.__name__})"
    log.append(f"Коэффициенты нелинейной зависимости от параметра: q = \n{'\n'.join([str(_) for _ in q[0]])}\n")

    def func(t):
        return q[1](t)

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

    return graphic.build(), log, (sum_diff, gamma), f"Нелинейная зависимость от параметра (метод {fit.__name__})"
