import os
import sys
from uuid import UUID

from compmath.views.settings import SettingsView


class SettingsController:

    def __init__(self, model, widgets_factory, parent):
        self.model = model
        self.view = SettingsView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

    def change_theme(self, theme_id: UUID):
        self.model.change_theme(theme_id)

    @staticmethod
    def reboot():
        # TODO: Пусть это вызывается в модели
        os.execl(sys.executable, sys.executable, *sys.argv)
