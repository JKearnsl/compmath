from compmath.api.slat import SLATClient
from compmath.models.slat.base import BaseSLATModel, TableRow


class ZModel(BaseSLATModel):

    def __init__(self, api_client: SLATClient):
        super().__init__()

        self._api_client = api_client
        self._api_client.zmCalculated.connect(self.process_values)
        self._api_client.zmError.connect(self.validation_error)

        self._title = "Метод Зейделя"
        self._description = "Метод Зейделя - модификация метода простых итераций"

        self.matrix: list[list[int | float]] = [
            [56.43, -8.54, 6.36, 9.76],
            [4.34, 48.87, 9.18, 43.48],
            [6.75, -8.93, 48.88, 56.92]
        ]

    def calc(self):
        self._api_client.calc_zm(
            self.a(),
            self.b(),
            self.eps,
            self.iters_limit,
            self.x0
        )

    def process_values(self, content: list[tuple[list[str], list[TableRow], str]]):
        self.results = content
        self.notify_observers()
