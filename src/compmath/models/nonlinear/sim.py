from compmath.models.nonlinear.base import BaseNoNLinearModel
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

    def calc(self, fx: str, interval: tuple[float, float], eps: float) -> tuple[float, int] | None:
        """
        Метод простых итераций
        # TODO одинаковы с ньютоном
        :param fx:
        :param interval:
        :param eps:
        :return:
        """
        function = make_callable(fx)
        a, b = interval

        if function(a) * function(b) > 0:
            self.raise_error("На данном интервале нет корней")
            return

        n = 0
        x = a
        while abs(function(x)) > eps:
            n += 1
            x = x - function(x) / self.derivative(fx, x)

        return x, n
