from compmath.api.ni import NIClient
from compmath.models.base import BaseGraphicModel
from compmath.models.graphic import Graphic
from compmath.utils.func import make_callable, FunctionValidateError


class InterModel(BaseGraphicModel):

    def __init__(self, api_client: NIClient):
        super().__init__()
        self.api_client = api_client
        self.api_client.intermediateCalculated.connect(self.process_values)
        self.api_client.intermediateError.connect(self.validation_error)

        self._title = "Промежуточные расчеты"
        self._fx = "sin(2*x**2 + 1)"
        self._interval = (0, 1)
        self._x_limits = (-2, 2)
        self._y_limits = (-2, 2)

        self.reference_result = None
        self.surface_area = None
        self.volume = None
        self.arc_length = None

    @property
    def title(self) -> str:
        return self._title

    def set_title(self, title: str):
        self._title = title
        self.notify_observers()

    @property
    def fx(self) -> str:
        return self._fx

    def set_fx(self, fx: str):
        try:
            make_callable(fx)
        except FunctionValidateError:
            self.validation_error("Инвалидная функция")
            return

        self._fx = fx
        self.graphics.clear()
        self.notify_observers()

    @property
    def interval(self) -> tuple[float | int, float | int]:
        return self._interval

    def set_interval(self, interval: tuple[float | int, float | int]):
        if not isinstance(interval, tuple):
            raise ValueError("Неверный интервал")

        if len(interval) != 2:
            raise ValueError("Неверный интервал")

        if not isinstance(interval[0], (int, float)) or not isinstance(interval[1], (int, float)):
            raise ValueError("Неверный интервал")

        if interval[0] >= interval[1]:
            self.validation_error("Неверный интервал")
            return

        self._interval = interval
        self.notify_observers()

    def calc(self):
        self.api_client.calc_intermediate(
            self.interval[0],
            self.interval[1],
            self.fx,
            self._x_limits,
            self._y_limits
        )

    def process_values(self, content: tuple[Graphic, float, float, float, float]) -> None:
        self.graphics.append(content[0])
        self.reference_result = content[1]
        self.surface_area = content[2]
        self.volume = content[3]
        self.arc_length = content[4]
        self.notify_observers()
