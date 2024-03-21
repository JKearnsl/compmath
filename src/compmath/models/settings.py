from uuid import UUID

from compmath.config import InIConfig
from compmath.models.base import BaseModel
from compmath.utils import theme as theme_utils


class SettingsModel(BaseModel):

    def __init__(self, config: InIConfig):
        super().__init__()
        self.config = config

        self.__loaded_themes = {}
        self.__error_themes = []

        self.load_themes()

    def load_themes(self) -> None:
        """
            Загрузить темы из директории
        """
        self.__loaded_themes, self.__error_themes = theme_utils.get_themes()

    def get_themes(self) -> dict[UUID, tuple[type, str, str]]:
        return self.__loaded_themes

    def get_error_themes(self) -> list[tuple[str, str]]:
        return self.__error_themes

    def change_theme(self, theme_uuid: UUID) -> None:
        new_theme = self.__loaded_themes.get(theme_uuid)
        if not new_theme:
            raise ValueError("Тема не найдена")

        self.config.raw["BASE"]["THEME_UUID"] = str(theme_uuid)
        self.config.save()
        self.config.reload()
