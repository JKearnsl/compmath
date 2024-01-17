from compmath.config import InIConfig
from compmath.views.widgets import WidgetsFactory
from compmath.views.main import MainView

from compmath.controllers.research import ResearchController
from compmath.models import ResearchModel, MenuItem
from compmath.controllers.nonlinear import NoNLinearController
from compmath.models import NoNLinearModel
from compmath.controllers.slat import SLATController
from compmath.models import SLATModel
from compmath.controllers.sne import SNEController
from compmath.models import SNEModel
from compmath.controllers.ni import NIController
from compmath.models import NIModel
from compmath.controllers.aif import AIFController
from compmath.models import AIFModel

from compmath.controllers.settings import SettingsController
from compmath.models.settings import SettingsModel


class MainController:

    def __init__(
            self,
            model: 'MainModel',
            widgets_factory: 'WidgetsFactory',
            config: 'InIConfig',
            app_controller
    ):
        self.model = model
        self.config = config
        self.widgets_factory = widgets_factory
        self.app_controller = app_controller
        self.view = MainView(self, model, widgets_factory)

        self.view.show()
        self.view.model_loaded()

    def show_settings(self):
        SettingsController(
            SettingsModel(self.config), self.widgets_factory, self.view
        )

    def show_page(self, page_id: MenuItem):
        match page_id:
            case MenuItem.RESEARCH:
                ResearchController(
                    ResearchModel(), self.widgets_factory, self.view
                )
            case MenuItem.NONLINEAR:
                NoNLinearController(
                    NoNLinearModel(), self.widgets_factory, self.view
                )
            case MenuItem.SLAT:
                SLATController(
                    SLATModel(), self.widgets_factory, self.view
                )
            case MenuItem.SNE:
                SNEController(
                    SNEModel(), self.widgets_factory, self.view
                )
            case MenuItem.NI:
                NIController(
                    NIModel(), self.widgets_factory, self.view
                )
            case MenuItem.AIF:
                AIFController(
                    AIFModel(), self.widgets_factory, self.view
                )
            case _:
                raise ValueError(f'Unknown page_id: {page_id}')

    def close(self):
        ...