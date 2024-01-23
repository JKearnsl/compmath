from compmath.models.slat.base import BaseSLATModel


class SIModel(BaseSLATModel):

    def __init__(self):
        super().__init__()

        self._title = "Метод простых итераций"

    def calc(self) -> None:
        ...