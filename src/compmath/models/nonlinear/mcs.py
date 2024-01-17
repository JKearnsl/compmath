from compmath.models.nonlinear.base import BaseNoNLinearModel
from compmath.utils.func import make_callable


class MCSModel(BaseNoNLinearModel):

    def __init__(self):
        super().__init__()
        self._title = "Метод хорд и секущих"
        self._description = """
            <p>
            Метод хорд и секущих — это простейший итерационный метод решения нелинейных уравнений.
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

        :param fx:
        :param interval:
        :param eps:
        :return:
        """
        function = make_callable(self.fx)
        a, b = self.interval

        if function(a) * function(b) > 0:
            self.raise_error("На данном интервале нет корней")
            return

        n = 0
        x = None
        while abs(a - b) > self.eps:
            n += 1
            x = a - (function(a) * (b - a)) / (function(b) - function(a))

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
