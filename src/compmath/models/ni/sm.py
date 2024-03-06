from collections import deque

from compmath.models.ni.base import BaseNIModel
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable


class SModel(BaseNIModel):

    def __init__(self):
        super().__init__()
        self._title = "Метод Симсона (парабол)"
        self._description = """
            <p>
            Метод Симпсона — это метод численного интегрирования функции, заключающийся в замене подынтегральной функции
            на многочлен второй степени, который совпадает с ней в левой, правой границах и середине отрезка
            интегрирования.
            </p>
        """
        self._fx = "sin(2*x**2 + 1)"
        self._interval = (0, 1)
        self._intervals = 10
        self._x_limits = (-2, 2)
        self._y_limits = (-2, 2)

    def calc(self, in_thread: bool = False) -> None:
        self.graphics.clear()
        self.table.clear()

        function = make_callable(self.fx)
        a, b = self.interval
        n = self.intervals

        if a > b:
            self.validation_error("Левая граница интервала не может быть больше правой")
            return

        if n % 2 != 0:
            self.validation_error("Количество интервалов должно быть четным")
            return

        graphic = Graphic(x_limits=self.x_limits, y_limits=self.y_limits)
        graphic.add_graph(function)
        graphic.add_graph(lambda x: 0, width=2, x_limits=(a, b))
        graphic.add_graph(fy=lambda y: a, width=2, y_limits=(function(a), 0))
        graphic.add_graph(fy=lambda y: b, width=2, y_limits=(function(b), 0))
        rows = deque(maxlen=1000)

        h = (b - a) / (2 * n)
        sum1 = 0
        sum2 = 0
        for i in range(2 * n):
            if i % 2 != 0:
                sum1 += function(a + i * h)
            elif i != 0:
                sum2 += function(a + i * h)

        result = h / 3 * (function(a) + 4 * sum1 + 2 * sum2 + function(b))

        self.graphics.append(graphic)
        self.table = list(rows)
        self.result = result

        if not in_thread:
            self.notify_observers()
