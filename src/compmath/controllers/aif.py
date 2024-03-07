from compmath.api.factory import APIFactory
from compmath.views.aif import AIFView
from compmath.views.widgets import WidgetsFactory


class AIFController:

    def __init__(self, model, widgets_factory: 'WidgetsFactory', api_factory: APIFactory, parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.api_factory = api_factory
        self.view = AIFView(self, self.model, widgets_factory, api_factory, parent)

        self.view.show()
        self.view.model_loaded()
