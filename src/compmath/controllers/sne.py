from compmath.views.sne import SNEView
from compmath.views.widgets import WidgetsFactory


class SNEController:

    def __init__(self, model, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = SNEView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()
