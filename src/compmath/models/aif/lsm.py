from compmath.models.aif.base import BaseAIFModel


class LSModel(BaseAIFModel):
    """
    Метод наименьших квадратов

    """

    def __init__(self):
        super().__init__()
        self._title = "Метод наименьших квадратов"
        self._description = """
            ...
        """
        self._points = [
            (-4.38, 2.25),
            (-3.84, 2.83),
            (-3.23, 3.44),
            (-2.76, 4.31),
            (-2.22, 5.29),
            (-1.67, 6.55),
            (-1.13, 8.01),
            (-0.60, 10.04)
        ]

    def calc(self) -> None:
        ...
        self.notify_observers()
