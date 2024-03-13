from compmath.api.ni import NIClient
from compmath.models.ni.base import BaseNIModel


class S1Model(BaseNIModel):

    def __init__(self, api_client: NIClient):
        super().__init__()
        self.api_client = api_client
        self.api_client.sm1Calculated.connect(self.process_values)
        self.api_client.sm1Error.connect(self.validation_error)

        self._title = "Метод Симпсона с равномерным шагом (1/3)"
        self._description = """
            <p>
            Данный метод использует квадратичные полиномы для аппроксимации подынтегральной функции на каждом 
            под интервале. Он разбивает интервал интегрирования на n равных частей и использует значения функции 
            в узлах разбиения для вычисления приближенного значения интеграла.
            </p>
        """
        self._fx = "sin(2*x**2 + 1)"
        self._interval = (0, 1)
        self._intervals = 10
        self._x_limits = (-2, 2)
        self._y_limits = (-2, 2)

    def calc(self):
        self.api_client.calc_sm1(
            self.interval[0],
            self.interval[1],
            self.intervals,
            self.fx,
            self._x_limits,
            self._y_limits
        )
