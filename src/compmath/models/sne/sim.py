from compmath.api.sne import SNEClient
from compmath.models.graphic import Graphic
from compmath.models.sne.base import BaseSNEModel, TableRow


class SIModel(BaseSNEModel):

    def __init__(self, api_client: SNEClient):
        super().__init__()
        self.api_client = api_client
        self.api_client.simCalculated.connect(self.process_values)
        self.api_client.simError.connect(self.validation_error)

        self._title = "Метод простых итераций"

    def calc(self):
        self.api_client.calc_sim(
            self.equations,
            self.eps,
            self._iters_limit,
            self.initial_guess,
            self.x_limits,
            self.y_limits
        )

    def process_values(self, content: tuple[Graphic, list[str], list[TableRow]]) -> None:
        self.graphics = content[0]
        self.solve_log = content[1]
        self.table = content[2]
        self.notify_observers()
