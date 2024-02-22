from compmath.models.nonlinear.base import BaseNoNLinearModel, TableRow
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable, derivative, tangent


class NTModel(BaseNoNLinearModel):
    def __init__(self):
        super().__init__()
        self._title = "Метод Ньютона (касательных)"
        self._description = """
            <p>
            Метод Ньютона — это простейший итерационный метод решения нелинейных уравнений.
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
        Метод Ньютона (касательных)

        :return:
        """
        self.graphics.clear()
        self.table.clear()

        function = make_callable(self.fx)
        a, b = self.interval

        if function(a) * function(b) > 0:
            self.validation_error("На данном интервале нет корней")
            return

        if function(a) * derivative(derivative(function))(a) > 0:
            x = a
        else:
            x = b

        n = 0
        while True:
            h = - function(x) / derivative(function)(x)
            x += h
            n += 1

            graphic = Graphic(x_limits=self.x_limits)
            graphic.add_graph(function)
            graphic.add_graph(tangent(function, x))
            graphic.add_point(x, function(x))
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

            if abs(h) <= self.eps or n >= self.iters_limit:
                break

        self.result = x
        self.iters = n
        self.notify_observers()
