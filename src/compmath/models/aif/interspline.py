from compmath.models.aif.base import BaseAIFModel
from compmath.models.graphic import Graphic
from compmath.utils.func import cspline, pspline, lspline


class InterSplineModel(BaseAIFModel):
    """
    Интерполяция: Сплайны

    """

    def __init__(self):
        super().__init__()
        self._title = "Интерполяция: Сплайны"
        self._description = """
            Интерполяция методами кубических, линейных и параболических сплайнов
        """
        self._points = [
            (0.43, 1.63597),
            (0.48, 1.73234),
            (0.55, 1.87686),
            (0.62, 2.03045),
            (0.70, 2.22846),
            (0.75, 2.35973)
        ]
        self._x = 0.645

    @property
    def x(self) -> float:
        return self._x

    def set_x(self, x: float) -> None:
        if self._x == x:
            return

        self._x = x
        self.notify_observers()

    def calc(self) -> None:
        self.results.clear()
        points = sorted(self.points, key=lambda _: _[0])

        self.results.append(self.cubic_spline(points))
        self.results.append(self.parabolic_spline(points))
        self.results.append(self.linear_spline(points))

        self.results.append(self.lagrange(points))

        self.notify_observers()

    def cubic_spline(self, points: list[tuple[float, float]]) -> tuple[Graphic, list[str], str]:
        """
        Кубический сплайн

        :param points: отсортированный двумерный массив точек (x, y)
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
        log = []

        x_data, y_data = zip(*points)

        # Кубический сплайн
        spline = cspline(x_data, y_data)
        log.append(f"Коэффициенты: \n{spline}")

        # График
        for point in points:
            graphic.add_point(*point)
        graphic.add_graph(spline)

        return graphic, log, "Кубический сплайн"

    def parabolic_spline(self, points: list[tuple[float, float]]) -> tuple[Graphic, list[str], str]:
        """
        Параболический сплайн

        :param points: отсортированный двумерный массив точек (x, y)
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
        log = []

        x_data, y_data = zip(*points)

        # Параболический сплайн
        spline = pspline(x_data, y_data)
        log.append(f"Коэффициенты: \n{spline}")

        # График
        for point in points:
            graphic.add_point(*point)
        graphic.add_graph(spline)

        return graphic, log, "Параболический сплайн"

    def linear_spline(self, points: list[tuple[float, float]]) -> tuple[Graphic, list[str], str]:
        """
        Линейный сплайн

        :param points: отсортированный двумерный массив точек (x, y)
        :return: график, лог
        """
        graphic = Graphic(self._x_limits, self._y_limits)
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

        return graphic, log, "Линейный сплайн"

    def lagrange(self, points: list[tuple[float, float]]) -> tuple[Graphic, list[str], str]:
        graphic = Graphic(self._x_limits, self._y_limits)
        log = []

        x_point = self.x
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

        return graphic, log, "Полином Лагранжа",
