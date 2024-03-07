from compmath_calc_server.models.graphic import GraphicBuilder, GraphicItem
from compmath_calc_server.models.aif.dto import InputInterpModel, ResultInterpItem
from compmath_calc_server.utils.func import cspline, pspline, lspline

type ItemSplineReturn = tuple[list[GraphicItem], list[str], str]


def calc(data: InputInterpModel) -> list[ResultInterpItem]:
    results = []
    points = sorted(data.points, key=lambda _: _[0])

    results.append(cubic_spline(points, data.x_limits, data.y_limits))
    results.append(parabolic_spline(points, data.x_limits, data.y_limits))
    results.append(linear_spline(points, data.x_limits, data.y_limits))

    results.append(lagrange(points, data.x_limits, data.y_limits, data.x))

    return [
        ResultInterpItem(
            graphic_items=result[0],
            log=result[1],
            title=result[2]
        ) for result in results
    ]


def cubic_spline(
        points: list[tuple[float, float]],
        x_limits: tuple[float | int, float | int],
        y_limits: tuple[float | int, float | int]
) -> ItemSplineReturn:
    """
    Кубический сплайн

    :param points: отсортированный двумерный массив точек (x, y)
    :param x_limits:
    :param y_limits:
    :return: график, лог
    """
    graphic = GraphicBuilder(x_limits, y_limits)
    log = []

    x_data, y_data = zip(*points)

    # Кубический сплайн
    spline = cspline(x_data, y_data)
    log.append(f"Коэффициенты: \n{spline}")

    # График
    for point in points:
        graphic.add_point(*point)
    graphic.add_graph(spline)

    return graphic.build(), log, "Кубический сплайн"


def parabolic_spline(
        points: list[tuple[float, float]],
        x_limits: tuple[float | int, float | int],
        y_limits: tuple[float | int, float | int]
) -> ItemSplineReturn:
    """
    Параболический сплайн

    :param points: отсортированный двумерный массив точек (x, y)
    :param x_limits:
    :param y_limits:
    :return: график, лог
    """
    graphic = GraphicBuilder(x_limits, y_limits)
    log = []

    x_data, y_data = zip(*points)

    # Параболический сплайн
    spline = pspline(x_data, y_data)
    log.append(f"Коэффициенты: \n{spline}")

    # График
    for point in points:
        graphic.add_point(*point)
    graphic.add_graph(spline)

    return graphic.build(), log, "Параболический сплайн"


def linear_spline(
        points: list[tuple[float, float]],
        x_limits: tuple[float | int, float | int],
        y_limits: tuple[float | int, float | int]
) -> ItemSplineReturn:
    """
    Линейный сплайн

    :param points: отсортированный двумерный массив точек (x, y)
    :param x_limits:
    :param y_limits:
    :return: график, лог
    """
    graphic = GraphicBuilder(x_limits, y_limits)
    log = []

    x_data, y_data = zip(*points)

    # Линейный сплайн
    spline = lspline(x_data, y_data)
    log.append(f"Коэффициенты: \n{spline}")

    def func(t): return spline(t)

    # График
    for point in points:
        graphic.add_point(*point)
    graphic.add_graph(func)

    return graphic.build(), log, "Линейный сплайн"


def lagrange(
        points: list[tuple[float, float]],
        x_limits: tuple[float | int, float | int],
        y_limits: tuple[float | int, float | int],
        x: float
) -> ItemSplineReturn:
    graphic = GraphicBuilder(x_limits, y_limits)
    log = []

    x_point = x
    x_vector, y_vector = zip(*points)

    s = 0
    for i in range(len(points)):
        p = 1
        for j in range(len(points)):
            if i != j:
                p = p * (x_point - x_vector[j]) / (x_vector[i] - x_vector[j])
        s += y_vector[i] * p

    log.append(f"Для x = {x_point}, y = {s}")

    for point in points:
        graphic.add_point(*point)
    graphic.add_point(x_point, s, color="blue")

    return graphic.build(), log, "Полином Лагранжа",