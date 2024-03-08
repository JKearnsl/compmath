from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from compmath.api.factory import APIFactory
from compmath.models import MenuItem
from compmath.models.ni.intermediate import InterModel
from compmath.models.ni.lrm import LRModel
from compmath.models.ni.mrm import MRModel
from compmath.models.ni.rrm import RRModel
from compmath.models.ni.sm import SModel
from compmath.models.ni.tm import TModel
from compmath.utils.observer import DObserver
from compmath.utils.ts_meta import TSMeta
from compmath.views.ni.interm_item import NItermView
from compmath.views.ni.item import NItemView
from compmath.views.ni.static_ui import UiNIPage

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class NIView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model, widgets_factory, api_factory: APIFactory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.api_factory = api_factory
        self.widgets_factory = widgets_factory

        parent.ui.content_layout.addWidget(self)
        parent.ui.content_layout.setCurrentWidget(self)

        self.ui = UiNIPage()
        self.ui.setup_ui(self, widgets_factory)

        # Регистрация представлений
        self.model.add_observer(self)

        # События

    def model_changed(self):
        inter = NItermView(InterModel(self.api_factory.create_ni()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(inter)

        lrm = NItemView(LRModel(self.api_factory.create_ni()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(lrm)

        rrm = NItemView(RRModel(self.api_factory.create_ni()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(rrm)

        mrm = NItemView(MRModel(self.api_factory.create_ni()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(mrm)

        tm = NItemView(TModel(self.api_factory.create_ni()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(tm)

        sm = NItemView(SModel(self.api_factory.create_ni()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(sm)

        inter.model_loaded()
        lrm.model_loaded()
        rrm.model_loaded()
        mrm.model_loaded()
        tm.model_loaded()
        sm.model_loaded()

    def model_loaded(self):
        self.model_changed()
