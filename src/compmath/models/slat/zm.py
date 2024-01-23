from compmath.models.slat.base import BaseSLATModel


class ZModel(BaseSLATModel):

    def __init__(self):
        super().__init__()

        self._title = "Метод Зейделя"
        self._description = "Метод Зейделя - модификация метода простых итераций..."

    def calc(self) -> None:
        ...