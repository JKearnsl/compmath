from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from compmath.api.factory import APIFactory
from compmath.models import MenuItem
from compmath.models.aif.alsm import ALSModel
from compmath.models.aif.interspline import InterSplineModel
from compmath.utils.observer import DObserver
from compmath.utils.ts_meta import TSMeta
from compmath.views.aif.approximation import AItemView
from compmath.views.aif.interpolation import InterItemView
from compmath.views.aif.static_ui import UiAIFPage

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class AIFView(QWidget, DObserver, metaclass=TSMeta):
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

        self.ui = UiAIFPage()
        self.ui.setup_ui(self, widgets_factory)

        # Регистрация представлений
        self.model.add_observer(self)

        # События

    def model_changed(self):
        ...

    def model_loaded(self):
        alsm = AItemView(ALSModel(self.api_factory.create_aif()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(alsm)

        inter = InterItemView(InterSplineModel(self.api_factory.create_aif()), self.widgets_factory, self)
        self.ui.central_layout.addWidget(inter)

        alsm.model_loaded()
        inter.model_loaded()

        self.model_changed()
