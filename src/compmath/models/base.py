from abc import ABC

from compmath.models.graphic import Graphic


class BaseModel(ABC):

    def __init__(self):
        self._mObservers = []

    def add_observer(self, observer):
        self._mObservers.append(observer)

    def remove_observer(self, observer):
        self._mObservers.remove(observer)

    def notify_observers(self):
        for observer in self._mObservers:
            observer.model_changed()

    def validation_error(self, error):
        for observer in self._mObservers:
            observer.validation_error(error)


class BaseGraphicModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._x_limits = (-10, 10)
        self._y_limits = (-10, 10)
        self.graphics: list[Graphic] = []

    @property
    def x_limits(self) -> tuple[float | int, float | int]:
        return self._x_limits

    @property
    def y_limits(self) -> tuple[float | int, float | int]:
        return self._y_limits

    def set_x_limits(self, x_limits: tuple[float | int, float | int]):
        if not isinstance(x_limits, tuple):
            raise ValueError("Неверно задан предел по X: тип не является кортежем")

        if len(x_limits) != 2:
            raise ValueError("Неверно задан предел по X: длина кортежа не равна 2")

        if not isinstance(x_limits[0], (int, float)) or not isinstance(x_limits[1], (int, float)):
            raise ValueError("Неверно задан предел по X: тип элементов кортежа не является int или float")

        if x_limits[0] >= x_limits[1]:
            self.validation_error("Неверно задан предел по X: левый предел больше или равен правому пределу")
            return

        self._x_limits = x_limits
        self.notify_observers()

    def set_y_limits(self, y_limits: tuple[float | int, float | int]):
        if not isinstance(y_limits, tuple):
            raise ValueError("Неверно задан предел по Y: тип не является кортежем")

        if len(y_limits) != 2:
            raise ValueError("Неверно задан предел по Y: длина кортежа не равна 2")

        if not isinstance(y_limits[0], (int, float)) or not isinstance(y_limits[1], (int, float)):
            raise ValueError("Неверно задан предел по Y: тип элементов кортежа не является int или float")

        if y_limits[0] >= y_limits[1]:
            self.validation_error("Неверно задан предел по Y: левый предел больше или равен правому пределу")
            return

        self._y_limits = y_limits
        self.notify_observers()

