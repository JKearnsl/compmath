from compmath.models.nonlinear.base import BaseNoNLinearModel, TableRow
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable


class HDModel(BaseNoNLinearModel):
    """
    Метод половинного деления

    """

    def __init__(self):
        super().__init__()
        self._title = "Метод половинного деления"
        self._description = """
            <p>
            Метод половинного деления — это простейший итерационный метод решения нелинейных уравнений.
            Предполагается, что функция <i>f(x)</i> непрерывна на отрезке <i>[a, b]</i> и на концах отрезка принимает 
            значения разных знаков. Тогда на этом отрезке гарантированно существует хотя бы один корень уравнения 
            <i>f(x) = 0</i>.
            </p>
        """
        self._fx = "0.5**x + 1 - (x-2)**2"
        self._interval = (0, 1)
        self._eps = 0.0001

    def calc(self) -> None:
        """
        Рассчитать

        :return:
        """
        self.graphics.clear()
        self.table.clear()

        function = make_callable(self.fx)
        a, b = self.interval

        if function(a) * function(b) > 0:
            self.validation_error("Корни f(a) и f(b) одного знака")
            return

        n = 0
        while abs(a - b) > self.eps and n < self.iters_limit:
            n += 1
            x = (a + b) / 2

            graphic = Graphic(x_limits=self.x_limits, y_limits=self.y_limits)
            graphic.add_graph(function)
            graphic.add_point(a, function(a), color='yellow')
            graphic.add_point(b, function(b), color='yellow')
            graphic.add_point(x, function(x), color='red')

            table_row = TableRow(
                iter_num=n,
                a=a,
                b=b,
                x=x,
                fx=function(x),
                fa=function(a),
                fb=function(b),
                distance=abs(a - b)
            )
            self.graphics.append(graphic)
            self.table.append(table_row)

            if function(a) * function(x) < 0:
                b = x
            else:
                a = x

        self.result = (a + b) / 2
        self.iters = n
        self.notify_observers()
