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
        # self._points = [
        #     (-4.38, 2.25),
        #     (-3.84, 2.83),
        #     (-3.23, 3.44),
        #     (-2.76, 4.31),
        #     (-2.22, 5.29),
        #     (-1.67, 6.55),
        #     (-1.13, 8.01),
        #     (-0.60, 10.04)
        # ]
        self._points = [
            (1.2, 2.59),
            (1.57, 2.06),
            (1.94, 1.58),
            (2.31, 1.25),
            (2.68, 0.91),
            (3.05, 0.66),
            (3.42, 0.38),
            (3.79, 0.21)
        ]

    def calc(self) -> None:
        self._api_client.calc_alsm(self._points, self._x_limits, self._y_limits)

    def process_values(self, content: list[tuple[Graphic, list[str], tuple[float, float], str]]) -> None:
        self.results = content
        self.notify_observers()
