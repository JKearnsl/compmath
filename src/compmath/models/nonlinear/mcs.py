from compmath.models.nonlinear.base import BaseNoNLinearModel, TableRow
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable, line_between_points


class MCSModel(BaseNoNLinearModel):

    def __init__(self):
        super().__init__()
        self._title = "Метод хорд"
        self._description = """
            <p>
            Метод хорд — это простейший итерационный метод решения нелинейных уравнений.
            Предполагается, что функция <i>f(x)</i> непрерывна на отрезке <i>[a, b]</i> и на концах отрезка принимает 
            значения разных знаков. Тогда на этом отрезке гарантированно существует хотя бы один корень уравнения 
            <i>f(x) = 0</i>.
            </p>
        """
        self._fx = "x**3 - 2*x - 5"
        self._interval = (2, 3)
        self._eps = 0.001

    def calc(self) -> None:
        """
        Метод хорд и секущих

        :return:
        """
        self.graphics.clear()
        self.table.clear()

        function = make_callable(self.fx)
        a, b = self.interval

        if function(a) * function(b) > 0:
            self.raise_error("На данном интервале нет корней")
            return

        n = 0
        x = None
        while abs(a - b) > self.eps and n < self.iters_limit:
            n += 1
            x = a - (function(a) * (b - a)) / (function(b) - function(a))

            graphic = Graphic(x_limits=self.x_limits)
            graphic.add_graph(function)
            graphic.add_graph(line_between_points(a, function(a), b, function(b)), x_limits=(a, b))
            graphic.add_point(x, function(x), color="red")
            graphic.add_point(a, function(a), color="yellow")
            graphic.add_point(b, function(b), color="yellow")
            self.graphics.append(graphic)

            self.table.append(
                TableRow(
                    iter_num=n,
                    x=x,
                    fx=function(x),
                    a=a,
                    fa=function(a),
                    b=b,
                    fb=function(b),
                    distance=abs(a - b)
                )
            )

            if function(x) == 0:
                break

            if function(a) * function(x) < 0:
                b = x
            else:
                a = x

            if abs(function(x)) < self.eps:
                break

        self.result = x
        self.iters = n
        self.notify_observers()
