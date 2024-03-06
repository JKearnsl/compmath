from collections import deque

from compmath.models.ni.base import BaseNIModel, TableRow
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable


class RRModel(BaseNIModel):

    def __init__(self):
        super().__init__()
        self._title = "Метод правых прямоугольников"
        self._description = """
            <p>
            Метод правых прямоугольников - это метод численного интегрирования, который использует значения функции
            в правых концах отрезков разбиения. Площадь под графиком функции на каждом отрезке разбиения аппроксимируется
            прямоугольником, высота которого равна значению функции в правом конце отрезка. Площадь таких прямоугольников
            суммируется, и это и есть приближенное значение интеграла.
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
        for i in range(n):
            x = a + i * h
            y = function(x + h)
            s = y * h
            result += s

            if n <= 100:
                graphic.add_rect(x, y, x + h, 0, color="red")

            if n <= 1000 or i == 0 or i == n - 1:
                rows.append(TableRow(i, x, y, s))

        graphic.add_graph(
            function,
            x_limits=(a, b),
            width=2,
            fill="red" if n > 100 else False
        )

        self.graphics.append(graphic)
        self.table = list(rows)
        self.result = result

        if not in_thread:
            self.notify_observers()
