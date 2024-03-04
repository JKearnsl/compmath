from compmath.models.nonlinear.base import BaseNoNLinearModel, TableRow
from compmath.models.graphic import Graphic
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
        self._fx = "0.5**x + 1 - (x-2)**2"
        self._interval = (0, 1)
        self._eps = 0.0001

    def calc(self) -> None:
        """
        Метод простых итераций

        :return:
        """
        self.graphics.clear()
        self.table.clear()

        function = make_callable(self.fx)
        a, b = self.interval

        # Проверка сходимости
        if abs(function(a)) > 1 or abs(function(b)) > 1:
            self.validation_error("Метод не сходится")
            return

        n = 0
        x = a
        while True:
            x0 = x
            x = function(x0)
            n += 1

            graphic = Graphic(x_limits=self.x_limits, y_limits=self.y_limits)
            graphic.add_graph(function)
            graphic.add_point(x0, x, color="red")
            self.graphics.append(graphic)

            self.table.append(
                TableRow(
                    iter_num=n,
                    x=x0,
                    fx=x,
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
        self.notify_observers()
