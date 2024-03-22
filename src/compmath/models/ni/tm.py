from compmath.api.ni import NIClient
from compmath.models.ni.base import BaseNIModel


class TModel(BaseNIModel):

    def __init__(self, api_client: NIClient):
        super().__init__()
        self.api_client = api_client
        self.api_client.tmCalculated.connect(self.process_values)
        self.api_client.tmError.connect(self.validation_error)

        self._title = "Метод трапеций"
        self._description = """
            <p>
            Метод трапеций — это метод численного интегрирования функции, заключающийся в замене подынтегральной функции
            на многочлен первой степени, который совпадает с ней в левой и правой границах отрезка интегрирования.
            </p>
        """
        self._fx = "sin(2*x**2 + 1)"
        self._interval = (0, 1)
        self._intervals = 10
        self._x_limits = (-2, 2)

    def calc(self):
        self.api_client.calc_tm(
            self.interval[0],
            self.interval[1],
            self.intervals,
            self.fx,
            self._x_limits,
            self._y_limits
        )
