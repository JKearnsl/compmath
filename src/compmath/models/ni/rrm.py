from compmath.api.ni import NIClient
from compmath.models.ni.base import BaseNIModel


class RRModel(BaseNIModel):

    def __init__(self, api_client: NIClient):
        super().__init__()
        self.api_client = api_client
        self.api_client.rrmCalculated.connect(self.process_values)
        self.api_client.rrmError.connect(self.validation_error)

        self._title = "Метод правых прямоугольников"
        self._description = """
            <p>
            Метод правых прямоугольников - это метод численного интегрирования, который использует значения функции
            в правых концах отрезков разбиения. Площадь под графиком функции на каждом отрезке разбиения аппроксимируется
            прямоугольником, высота которого равна значению функции в правом конце отрезка. Площадь таких прямоугольников
            суммируется, и это и есть приближенное значение интеграла.
            </p>
        """
        self._fx = "sin(2*x**2 + 1)"
        self._interval = (0, 1)
        self._intervals = 10
        self._x_limits = (-2, 2)
        self._y_limits = (-2, 2)

    def calc(self):
        self.api_client.calc_rrm(
            self.interval[0],
            self.interval[1],
            self.intervals,
            self.fx,
            self._x_limits,
            self._y_limits
        )
