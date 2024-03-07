from compmath.api.aif import AIFClient
from compmath.models.aif.base import BaseAIFModel
from compmath.models.graphic import Graphic


class InterSplineModel(BaseAIFModel):
    """
    Интерполяция: Сплайны

    """

    def __init__(self, api_client: AIFClient):
        super().__init__()
        self._api_client = api_client
        self._api_client.interpCalculated.connect(self.process_values)
        self._api_client.interpError.connect(self.validation_error)

        self._title = "Интерполяция: Сплайны"
        self._description = """
            Интерполяция методами кубических, линейных и параболических сплайнов
        """
        self._points = [
            (0.43, 1.63597),
            (0.48, 1.73234),
            (0.55, 1.87686),
            (0.62, 2.03045),
            (0.70, 2.22846),
            (0.75, 2.35973)
        ]
        self._x = 0.645

    @property
    def x(self) -> float:
        return self._x

    def set_x(self, x: float) -> None:
        if self._x == x:
            return

        self._x = x
        self.notify_observers()

    def calc(self) -> None:
        self._api_client.calc_interp(self._points, self._x_limits, self._y_limits, self._x)

    def process_values(self, content: list[tuple[Graphic, list[str], str]]) -> None:
        self.results = content
        self.notify_observers()
