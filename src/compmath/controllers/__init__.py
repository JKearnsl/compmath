from compmath.api.factory import APIFactory
from compmath.config import InIConfig
from compmath.views.widgets import WidgetsFactory

from compmath.controllers.main import MainController
from compmath.models import MainModel


class ApplicationController:
    """
        Mediator between controllers

    """

    def __init__(
            self,
            widgets_factory: WidgetsFactory,
            api_factory: APIFactory,
            config: InIConfig,
    ):
        self.widgets_factory = widgets_factory
        self.api_factory = api_factory
        self.config = config

    def main(self):
        MainController(
            MainModel(
                is_debug=self.config.VAR.BASE.DEBUG,
                app_title=self.config.VAR.BASE.APP_NAME,
                app_version=self.config.VAR.VERSION,
                contact=self.config.VAR.BASE.CONTACT,
            ),
            self.widgets_factory,
            self.api_factory,
            self.config,
            self
        )
