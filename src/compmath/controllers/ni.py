from compmath.views.ni import NIView
from compmath.views.widgets import WidgetsFactory


class NIController:

    def __init__(self, model, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = NIView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()
