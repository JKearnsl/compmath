from collections import deque

from compmath.models.ni.base import BaseNIModel, TableRow
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable


class TModel(BaseNIModel):

    def __init__(self):
        super().__init__()
        self._title = "Метод трапеций"
        self._description = """
            <p>
            Метод трапеций — это метод численного интегрирования функции, заключающийся в замене подынтегральной функции
            на многочлен первой степени, который совпадает с ней в левой и правой границах отрезка интегрирования.
            </p>
        """
        self._fx = "x**3 - 2*x - 5"
        self._interval = (2, 3)
        self._intervals = 10
        self._x_limits = (1, 20)
        self._y_limits = (-10, 20)

    def calc(self, in_thread: bool = False) -> None:
        self.graphics.clear()
        self.table.clear()

        function = make_callable(self.fx)
        a, b = self.interval
        n = self.intervals

        if a > b:
            self.validation_error("Левая граница интервала не может быть больше правой")
            return

        if function(a) * function(b) > 0:
            self.validation_error("На данном интервале нет корней")
            return

        graphic = Graphic(x_limits=self.x_limits, y_limits=self.y_limits)
        graphic.add_graph(function)
        graphic.add_graph(lambda x: 0, width=2)
        graphic.add_graph(fy=lambda y: a, width=2, y_limits=(function(a), 0))
        graphic.add_graph(fy=lambda y: b, width=2, y_limits=(function(b), 0))

        rows = deque(maxlen=1000)

        h = (b - a) / n
        result = 0
        for i in range(1, n + 1):
            x = a + i * h
            y = function(x)
            y_prev = function(x - h)
            delta_t = x - (x - h)

            s = ((y + y_prev) / 2) * delta_t
            result += s

            if n <= 100:
                graphic.add_polygon(
                    [
                        (x - h, 0),
                        (x, 0),
                        (x, y),
                        (x - h, y_prev)
                    ],
                    color="red",
                    width=2
                )

            if n <= 1000:
                rows.append(TableRow(i, x, y, s))

        graphic.add_graph(
            function,
            x_limits=(a, b),
            width=2,
            fill="red" if n > 100 else False
        )

        if n > 1000:
            rows.append(TableRow(0, a, function(a), 0))
            rows.append(TableRow(n, b, function(b), result))

        self.graphics.append(graphic)
        self.table = list(rows)
        self.result = result

        if not in_thread:
            self.notify_observers()