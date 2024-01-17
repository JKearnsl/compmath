from compmath.config import InIConfig
from compmath.models.base import BaseModel
from compmath.utils import theme as theme_utils


class SettingsModel(BaseModel):

    def __init__(self, config: InIConfig):
        super().__init__()
        self.config = config

        self.__loaded_themes = dict()
        self.__error_themes = list()

        self.load_themes()

    def load_themes(self) -> None:
        """
            Загрузить темы из директории
        """
        self.__loaded_themes, self.__error_themes = theme_utils.get_themes()

    def get_themes(self) -> dict[str, tuple[type, str, str]]:
        return self.__loaded_themes

    def get_error_themes(self) -> list[tuple[str, str]]:
        return self.__error_themes

    def change_theme(self, theme_title: str) -> None:
        new_theme = self.__loaded_themes.get(theme_title)
        if not new_theme:
            raise ValueError("Тема не найдена")

        self.config.raw["BASE"]["THEME_TITLE"] = theme_title
        self.config.save()
        self.config.reload()

    def add_observer(self, observer):
        self._mObservers.append(observer)

    def remove_observer(self, observer):
        self._mObservers.remove(observer)

    def notify_observers(self):
        for observer in self._mObservers:
            observer.model_changed()
            