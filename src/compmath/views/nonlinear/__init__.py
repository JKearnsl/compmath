from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from compmath.models import MenuItem
from compmath.models.nonlinear.hdm import HDModel
from compmath.models.nonlinear.mcs import MCSModel
from compmath.models.nonlinear.mcs_one import MCSOneModel
from compmath.models.nonlinear.mcs_two import MCSTwoModel
from compmath.models.nonlinear.ntm import NTModel
from compmath.models.nonlinear.sim import SIModel
from compmath.utils.observer import DObserver
from compmath.utils.ts_meta import TSMeta
from compmath.views.nonlinear.item import NoNLinearItemView
from compmath.views.nonlinear.static_ui import UINoNLinearPage

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class NoNLinearView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model, widgets_factory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        parent.ui.content_layout.addWidget(self)
        parent.ui.content_layout.setCurrentWidget(self)

        self.ui = UINoNLinearPage()
        self.ui.setup_ui(self, widgets_factory)

        # Регистрация представлений
        self.model.add_observer(self)

        # События

    def model_changed(self):
        ...

    def model_loaded(self):
        hdm = NoNLinearItemView(HDModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(hdm)

        mcs = NoNLinearItemView(MCSModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(mcs)

        mcs_one = NoNLinearItemView(MCSOneModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(mcs_one)

        mcs_two = NoNLinearItemView(MCSTwoModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(mcs_two)

        ntm = NoNLinearItemView(NTModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(ntm)

        sim = NoNLinearItemView(SIModel(), self.widgets_factory, self)
        self.ui.central_layout.addWidget(sim)

        hdm.model_loaded()
        mcs.model_loaded()
        mcs_one.model_loaded()
        mcs_two.model_loaded()
        ntm.model_loaded()
        sim.model_loaded()

        self.model_changed()
