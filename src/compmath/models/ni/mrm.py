from compmath.api.ni import NIClient
from compmath.models.graphic import Graphic
from compmath.models.ni.base import BaseNIModel, TableRow


class MRModel(BaseNIModel):

    def __init__(self, api_client: NIClient):
        super().__init__()
        self.api_client = api_client
        self.api_client.mrmCalculated.connect(self.process_values)
        self.api_client.mrmError.connect(self.validation_error)

        self._title = "Метод средних прямоугольников"
        self._description = """
            <p>
            Метод средних прямоугольников — это метод численного интегрирования функции, заключающийся в замене
            подынтегральной функции на многочлен нулевой степени, который совпадает с ней в середине отрезка
            интегрирования.
            </p>
        """
        self._fx = "sin(2*x**2 + 1)"
        self._interval = (0, 1)
        self._intervals = 10
        self._x_limits = (-2, 2)
        self._y_limits = (-2, 2)

    def calc(self):
        self.api_client.calc_mrm(
            self.interval[0],
            self.interval[1],
            self.intervals,
            self.fx,
            self._x_limits,
            self._y_limits
        )

    def process_values(self, content: tuple[Graphic, list[TableRow], float]) -> None:
        self.graphics.append(content[0])
        self.table = content[1]
        self.result = content[2]
        self.notify_observers()
