from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from compmath.api.factory import APIFactory
from compmath.models import MenuItem
from compmath.models.slat.gm import GModel
from compmath.models.slat.sim import SIModel
from compmath.models.slat.zm import ZModel
from compmath.utils.observer import DObserver
from compmath.utils.ts_meta import TSMeta
from compmath.views.slat.static_ui import UiSLATPage
from compmath.views.slat.item import SLATItemView

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class SLATView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model, widgets_factory, api_factory: APIFactory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory
        self.api_factory = api_factory

        parent.ui.content_layout.addWidget(self)
        parent.ui.content_layout.setCurrentWidget(self)

        self.ui = UiSLATPage()
        self.ui.setup_ui(self, widgets_factory)

        # Регистрация представлений
        self.model.add_observer(self)

        # События

    def model_changed(self):
        ...

    def model_loaded(self):
        sim = SLATItemView(SIModel(api_client=self.api_factory.create_slat()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(sim)

        zm = SLATItemView(ZModel(api_client=self.api_factory.create_slat()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(zm)

        gm = SLATItemView(GModel(api_client=self.api_factory.create_slat()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(gm)

        sim.model_loaded()
        zm.model_loaded()
        gm.model_loaded()

        self.model_changed()
