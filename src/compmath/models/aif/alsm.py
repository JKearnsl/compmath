from compmath.api.aif import AIFClient
from compmath.models.aif.base import BaseAIFModel
from compmath.models.graphic import Graphic


class ALSModel(BaseAIFModel):
    """
    Аппроксимация: Метод наименьших квадратов

    """

    def __init__(self, api_client: AIFClient):
        super().__init__()
        self._api_client = api_client
        self._api_client.alsmCalculated.connect(self.process_values)
        self._api_client.alsmError.connect(self.validation_error)

        self._title = "Аппроксимация: Метод наименьших квадратов"
        self._description = """
            Включает в себя методы линейной регрессии, полиномиальной регрессии, 
            линейной комбинации линейно-независимых функций, нелинейной зависимости от параметра.
        """

        self._points = [
            (1.0, 0.28),
            (1.64, 0.19),
            (2.28, 0.15),
            (2.91, 0.11),
            (3.56, 0.09),
            (4.19, 0.08),
            (4.84, 0.07),
            (5.58, 0.06)
        ]

    def calc(self) -> None:
        self._api_client.calc_alsm(self._points, self._x_limits, self._y_limits)

    def process_values(self, content: list[tuple[Graphic, list[str], tuple[float, float], str]]) -> None:
        self.results = content
        self.notify_observers()
