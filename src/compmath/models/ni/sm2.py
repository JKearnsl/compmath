from compmath.api.ni import NIClient
from compmath.models.ni.base import BaseNIModel


class S2Model(BaseNIModel):

    def __init__(self, api_client: NIClient):
        super().__init__()
        self.api_client = api_client
        self.api_client.sm2Calculated.connect(self.process_values)
        self.api_client.sm2Error.connect(self.validation_error)

        self._title = "Метод Симпсона 3/8"
        self._description = """
            <p>
            Данный метод использует кубические полиномы для аппроксимации подынтегральной функции на каждом 
            под интервале. Он также разбивает интервал интегрирования, но на 2n частей. 
            Использует разные весовые коэффициенты для вычисления суммы, включая 4 для значений функции в нечётных 
            точках и 2 для значений функции в чётных точках, кроме первой и последней точек, 
            которые учитываются с коэффициентами 1.
            </p>
        """
        self._fx = "sin(2*x**2 + 1)"
        self._interval = (0, 1)
        self._intervals = 10
        self._x_limits = (-2, 2)
        self._y_limits = (-2, 2)

    def calc(self):
        self.api_client.calc_sm2(
            self.interval[0],
            self.interval[1],
            self.intervals,
            self.fx,
            self._x_limits,
            self._y_limits
        )
