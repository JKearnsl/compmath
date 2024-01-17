import atexit
import os
import shutil
import sys
import tempfile

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QStyleFactory

from compmath.config import InIConfig
from compmath.controllers import ApplicationController
from compmath.themes import BASE_THEME
from compmath.utils.theme import get_themes
from compmath.views.widgets import WidgetsFactory


class CompMathApp(QApplication):
    def __init__(self, *args):
        super().__init__(*args)
        data_path = os.path.join(os.path.expanduser("~"), ".compmath")
        tempfile.tempdir = os.path.join(data_path, "tmp", str(os.getpid()))
        os.makedirs(tempfile.tempdir, exist_ok=True)
        atexit.register(lambda: shutil.rmtree(tempfile.tempdir))

        QApplication.setDesktopSettingsAware(False)
        self.setStyle(QStyleFactory.create("Fusion"))

        QtCore.QDir.addSearchPath('icons', 'assets/icons')

        if os.path.exists("../../config.ini"):
            config_path = "../../config.ini"
        elif os.path.exists(os.path.join(data_path, "config.ini")):
            config_path = os.path.join(data_path, "config.ini")
        else:
            raise FileNotFoundError("Файл конфигурации не найден")

        config = InIConfig(config_path)

        self.setApplicationName(config.VAR.BASE.APP_NAME)
        self.setApplicationDisplayName(config.VAR.BASE.APP_NAME)
        self.setOrganizationName("jkearnsl")
        self.setOrganizationDomain("jkearnsl")
        self.setApplicationVersion(config.VAR.VERSION)
        self.setDesktopFileName(f"jkearnsl.{config.VAR.BASE.APP_NAME}")

        # Application icon
        app_icon = QtGui.QIcon()
        app_icon.addFile("icons:logo-32.png", QtCore.QSize(32, 32))
        app_icon.addFile("icons:logo-64.png", QtCore.QSize(64, 64))
        app_icon.addFile("icons:logo-128.png", QtCore.QSize(128, 128))
        app_icon.addFile("icons:logo-256.png", QtCore.QSize(256, 256))
        self.setWindowIcon(app_icon)

        # Для сессии Wayland необходимо установить .desktop файл
        # Источники:
        # - https://github.com/OpenShot/openshot-qt/pull/3354
        # - https://github.com/openscad/openscad/blob/master/src/openscad.cc#L724
        # - https://github.com/openscad/openscad/issues/4505
        # - https://specifications.freedesktop.org/desktop-entry-spec/latest/ar01s02.html
        # - https://nicolasfella.de/posts/fixing-wayland-taskbar-icons/
        # - https://github.com/PhotoFlare/photoflare/pull/465/files#diff-c1c1d39b766177a787f02a2fd79839ceb5db497c09348db95001752e5f5b0dde
        # - https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html
        # Для Windows необходимо установить .ico файл, а также app_id:
        # - https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
        # И иконку рабочего стола:
        # - https://askubuntu.com/questions/476981/how-do-i-make-a-desktop-icon-to-launch-a-program

        theme = get_themes()[0].get(config.VAR.BASE.THEME_TITLE)
        if not theme:
            theme = BASE_THEME

        widgets_factory = WidgetsFactory(theme[0])

        controller = ApplicationController(
            widgets_factory=widgets_factory,
            config=config,
        )
        controller.main()

        self.exec()


if __name__ == '__main__':
    CompMathApp(sys.argv)
