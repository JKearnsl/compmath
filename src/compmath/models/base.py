from abc import ABC


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

    def raise_error(self, error):
        for observer in self._mObservers:
            observer.error_handler(error)
