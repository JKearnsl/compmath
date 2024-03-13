from compmath.api.ni import NIClient
from compmath.models.ni.base import BaseNIModel


class SModel(BaseNIModel):

    def __init__(self, api_client: NIClient):
        super().__init__()
        self.api_client = api_client
        self.api_client.smCalculated.connect(self.process_values)
        self.api_client.smError.connect(self.validation_error)

        self._title = "Метод Симсона (парабол)"
        self._description = """
            <p>
            Метод Симпсона — это метод численного интегрирования функции, заключающийся в замене подынтегральной функции
            на многочлен второй степени, который совпадает с ней в левой, правой границах и середине отрезка
            интегрирования.
            </p>
        """
        self._fx = "sin(2*x**2 + 1)"
        self._interval = (0, 1)
        self._intervals = 10
        self._x_limits = (-2, 2)
        self._y_limits = (-2, 2)

    def calc(self):
        self.api_client.calc_sm(
            self.interval[0],
            self.interval[1],
            self.intervals,
            self.fx,
            self._x_limits,
            self._y_limits
        )
