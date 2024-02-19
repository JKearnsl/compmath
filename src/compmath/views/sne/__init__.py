from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from compmath.models import MenuItem
from compmath.models.sne.ntm import NTModel
from compmath.models.sne.sim import SIModel
from compmath.models.sne.zm import ZModel
from compmath.utils.observer import DObserver
from compmath.utils.ts_meta import TSMeta
from compmath.views.sne.item import SNEItemView
from compmath.views.sne.static_ui import UiSNEPage

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class SNEView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model, widgets_factory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        parent.ui.content_layout.addWidget(self)
        parent.ui.content_layout.setCurrentWidget(self)

        self.ui = UiSNEPage()
        self.ui.setup_ui(self, widgets_factory)

        # Регистрация представлений
        self.model.add_observer(self)

        # События

    def model_changed(self):
        ...

    def model_loaded(self):
        sim = SNEItemView(SIModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(sim)

        zm = SNEItemView(ZModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(zm)

        ntm = SNEItemView(NTModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(ntm)

        sim.model_loaded()
        zm.model_loaded()
        ntm.model_loaded()

        self.model_changed()
