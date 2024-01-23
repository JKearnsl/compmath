from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from compmath.models import MenuItem
from compmath.models.slat.sim import SIModel
from compmath.models.slat.zm import ZModel
from compmath.utils.observer import DObserver
from compmath.utils.ts_meta import TSMeta
from compmath.views.slat.static_ui import UiSLATPage
from compmath.views.slat.item import SLATItemView

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class SLATView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model, widgets_factory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

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
        sim = SLATItemView(SIModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(sim)

        zm = SLATItemView(ZModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(zm)

        sim.model_loaded()
        zm.model_loaded()

        self.model_changed()