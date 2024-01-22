from compmath.models.nonlinear.base import BaseNoNLinearModel, TableRow
from compmath.models.nonlinear.graphic import Graphic
from compmath.utils.func import make_callable


class SIModel(BaseNoNLinearModel):
    def __init__(self):
        super().__init__()
        self._title = "Метод простых итераций"
        self._description = """
            <p>
            Метод простых итераций — это простейший итерационный метод решения нелинейных уравнений.
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
        Метод простых итераций

        :return:
        """
        self.graphics.clear()
        self.table.clear()

        function = make_callable(self.fx)
        a, b = self.interval

        n = 0
        x = a
        while True:
            x0 = x + 2 * self.eps
            x = function(x0)
            n += 1

            graphic = Graphic(x_limits=self.x_limits)
            graphic.add_graph(function)
            graphic.add_point(x, function(x), color="red")
            self.graphics.append(graphic)

            self.table.append(
                TableRow(
                    iter_num=n,
                    x=x,
                    fx=function(x),
                    distance=abs(x - x0),
                    a=x0,
                    b=None,
                    fa=function(a),
                    fb=None,
                )
            )

            if abs(x - x0) <= self.eps or n >= self.iters_limit:
                break

        self.result = x
        self.iters = n
        self.was_calculated()
