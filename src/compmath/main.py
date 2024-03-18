import atexit
import logging
import os
import shutil
import socket
import sys
import tempfile
from subprocess import Popen

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QStyleFactory

from compmath.api.factory import APIFactory
from compmath.config import InIConfig
from compmath.controllers import ApplicationController
from compmath.themes import BASE_THEME
from compmath.utils.theme import get_themes
from compmath.views.widgets import WidgetsFactory

import psutil


def kill_procs(host: str, port: int):
    ip = socket.gethostbyname(host)
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            conns = proc.connections("inet4")
        except psutil.AccessDenied:
            continue

        for conn in conns:
            if conn.laddr.port == port and conn.laddr.ip == ip:
                proc.kill()


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

        # Application settings
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

        # CompMath Calc Server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            is_port_in_use = s.connect_ex((config.VAR.CALC_SERVER.HOST, config.VAR.CALC_SERVER.PORT)) == 0

        if is_port_in_use:
            logging.warning(f"Port {config.VAR.CALC_SERVER.PORT} is already in use")
            logging.warning("Trying to terminate the process")
            kill_procs(config.VAR.CALC_SERVER.HOST, config.VAR.CALC_SERVER.PORT)
            logging.warning("Process terminated")

        subprocess = Popen(
            [
                "gunicorn",
                "--bind",
                f"{config.VAR.CALC_SERVER.HOST}:{config.VAR.CALC_SERVER.PORT}",
                "--workers",
                "3",
                "--worker-class",
                "uvicorn.workers.UvicornWorker",
                "compmath_calc_server.main:application"
            ]
        )
        atexit.register(subprocess.terminate)

        # Theme
        theme = get_themes()[0].get(config.VAR.BASE.THEME_UUID)
        if not theme:
            theme = BASE_THEME

        widgets_factory = WidgetsFactory(theme[0])
        api_factory = APIFactory(
            host=config.VAR.CALC_SERVER.HOST,
            port=config.VAR.CALC_SERVER.PORT,
            scheme="http",
            path="/api"
        )
        controller = ApplicationController(
            widgets_factory=widgets_factory,
            api_factory=api_factory,
            config=config,
        )
        controller.main()

        self.exec()


if __name__ == '__main__':
    CompMathApp(sys.argv)
