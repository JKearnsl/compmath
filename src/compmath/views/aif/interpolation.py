from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QHBoxLayout

from compmath.models.aif.interspline import InterSplineModel
from compmath.views.aif import AItemView
from compmath.views.widgets import WidgetsFactory


class InterItemView(AItemView):
    def __init__(
            self,
            model: InterSplineModel,
            widgets_factory: WidgetsFactory,
            parent=None
    ):
        super().__init__(model, widgets_factory, parent)
        self.model = model
        x_label = self.widgets_factory.label("x")
        x_input = self.widgets_factory.line_edit()
        self.x_input = x_input
        self.form.addRow(x_label, x_input)

        # События
        x_input.textChanged.connect(self.x_input_changed)

    def model_changed(self):
        self.x_input.blockSignals(True)
        self.x_input.setText(str(self.model.x))
        self.x_input.blockSignals(False)
        super().model_changed()

    def model_loaded(self):
        super().model_loaded()

    def x_input_changed(self):
        try:
            x = float(self.x_input.text())
        except ValueError:
            x = 0.0
        self.model.set_x(x)

    def show_result(self):
        modal = self.widgets_factory.modal(self.parent)
        modal.setFixedWidth(800)
        modal.setFixedHeight(600)
        modal.layout().setContentsMargins(5, 0, 5, 5)

        sheet = QWidget(modal)
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
            QWidget#sheet {
                background-color: transparent;
            }
        """)
        modal.layout().addWidget(sheet)

        central_layout = QVBoxLayout(sheet)
        central_layout.setContentsMargins(30, 20, 30, 20)
        central_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        central_layout.setSpacing(10)
        sheet.setLayout(central_layout)

        scroll_area = QScrollArea(modal)
        scroll_area.setFixedHeight(550)
        scroll_area.setObjectName("scroll_area")
        scroll_area.setStyleSheet("""
            QScrollArea#scroll_area {
                border: none;
                outline: none;
                background-color: transparent;
            }
        """)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(sheet)
        modal.layout().addWidget(scroll_area)

        for number, item in enumerate(self.model.results, 1):
            graphic, log, title = item

            item_widget = QWidget()
            central_layout.addWidget(item_widget)
            item_widget.setObjectName(f"item{number}_widget")
            item_widget.setStyleSheet("""
                QWidget#item$NUMBER_widget {
                    background-color: transparent;
                }
            """.replace(
                "$NUMBER", str(number)
            ))
            main_layout = QVBoxLayout(item_widget)
            main_layout.setContentsMargins(15, 0, 15, 15)
            main_layout.setSpacing(0)

            header_layout = self.widgets_factory.heading3(f"№{number}. {title}")
            main_layout.addWidget(header_layout)

            content_layout = QHBoxLayout()
            content_layout.setContentsMargins(5, 5, 5, 0)
            content_layout.setSpacing(10)
            main_layout.addLayout(content_layout)

            text_layout = QVBoxLayout()
            text_layout.setContentsMargins(0, 0, 0, 0)
            text_layout.setSpacing(0)
            content_layout.addLayout(text_layout)

            log_area = self.widgets_factory.textarea()
            log_area.setFixedHeight(300)
            log_area.setReadOnly(True)
            log_area.setPlainText("\n".join(log))
            text_layout.addWidget(log_area)

            graphic_widget = self.widgets_factory.graphic()
            graphic_widget.setFixedSize(QSize(300, 300))
            graphic_widget.add_plot(graphic.plot_items())
            graphic_widget.graphic_slider.setEnabled(False)
            content_layout.addWidget(graphic_widget)

        modal.exec()