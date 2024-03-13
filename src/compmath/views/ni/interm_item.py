from PyQt6 import sip
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout
)

from compmath.models.ni.intermediate import InterModel
from compmath.views.widgets import WidgetsFactory


class NItermView(QWidget):
    def __init__(
            self,
            model: InterModel,
            widgets_factory: WidgetsFactory,
            parent=None
    ):
        super().__init__(parent)
        self.widgets_factory = widgets_factory
        self.parent = parent
        self.model = model
        model.add_observer(self)

        self.setMaximumHeight(550)
        self.setMaximumWidth(600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        header = widgets_factory.heading4()
        layout.addWidget(header)
        self.header = header

        error_layout = QHBoxLayout()
        error_layout.setContentsMargins(10, 0, 10, 0)
        layout.addLayout(error_layout)

        error_label = widgets_factory.label()
        error_label.setWordWrap(True)
        error_label.setTextFormat(Qt.TextFormat.RichText)
        error_label.setFixedHeight(15)
        error_label.setFixedWidth(200)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("""
            QLabel {
                color: red;
                padding: 0px;
                margin: 0px;
            }
        """)
        self.error_label = error_label
        error_layout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignLeft)

        bottom = QHBoxLayout()
        bottom.setContentsMargins(10, 0, 10, 10)
        bottom.setSpacing(20)
        layout.addLayout(bottom)

        left = QVBoxLayout()
        left.setContentsMargins(0, 5, 0, 0)
        left.setAlignment(Qt.AlignmentFlag.AlignTop)
        left.setSpacing(20)
        bottom.addLayout(left)

        form_stub = QWidget()
        left.addWidget(form_stub)
        form = QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(10)
        form.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        form_stub.setLayout(form)

        fx_label = widgets_factory.label("f(x) = ")
        fx_input = widgets_factory.line_edit()
        self.fx_input = fx_input
        form.addRow(fx_label, fx_input)

        double_validator = QDoubleValidator()
        double_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))

        interval_a_label = widgets_factory.label("a = ")
        interval_a_input = widgets_factory.line_edit()
        interval_a_input.setValidator(double_validator)
        self.interval_a_input = interval_a_input
        form.addRow(interval_a_label, interval_a_input)

        interval_b_label = widgets_factory.label("b = ")
        interval_b_input = widgets_factory.line_edit()
        interval_b_input.setValidator(double_validator)
        self.interval_b_input = interval_b_input
        form.addRow(interval_b_label, interval_b_input)

        reference_result_label = widgets_factory.label("Эталон: ")
        reference_result_input = widgets_factory.line_edit()
        reference_result_input.setReadOnly(True)
        self.reference_result_input = reference_result_input
        form.addRow(reference_result_label, reference_result_input)

        surface_area_label = widgets_factory.label("S поверх: ")
        surface_area_input = widgets_factory.line_edit()
        surface_area_input.setReadOnly(True)
        self.surface_area_input = surface_area_input
        form.addRow(surface_area_label, surface_area_input)

        volume_label = widgets_factory.label("Объем тела: ")
        volume_input = widgets_factory.line_edit()
        volume_input.setReadOnly(True)
        self.volume_input = volume_input
        form.addRow(volume_label, volume_input)

        arc_length_label = widgets_factory.label("Длина дуги: ")
        arc_length_input = widgets_factory.line_edit()
        arc_length_input.setReadOnly(True)
        self.arc_length_input = arc_length_input
        form.addRow(arc_length_label, arc_length_input)

        calc_button = widgets_factory.button("Рассчитать")
        calc_button.setMaximumWidth(200)
        calc_button.setMinimumWidth(180)
        left.addWidget(calc_button)
        self.calc_button = calc_button

        graphic = widgets_factory.gl_widget()
        graphic.setFixedWidth(350)
        graphic.setFixedHeight(350)
        self.graphic = graphic
        bottom.addWidget(graphic)

        self.background_jobs = []

        # События
        fx_input.textChanged.connect(lambda text: self.model.set_fx(text))
        interval_a_input.textChanged.connect(self.interval_input_changed)
        interval_b_input.textChanged.connect(self.interval_input_changed)
        calc_button.clicked.connect(self.calc_button_clicked)

    def model_changed(self):
        if not self and sip.isdeleted(self):
            return

        self.error_label.setText("")

        if self.model.reference_result:
            self.reference_result_input.setText(str(self.model.reference_result))
            self.in_normal_state()
            self.reference_result_input.setCursorPosition(0)

        if self.model.surface_area:
            self.surface_area_input.setText(str(self.model.surface_area))
            self.surface_area_input.setCursorPosition(0)

        if self.model.volume:
            self.volume_input.setText(str(self.model.volume))
            self.volume_input.setCursorPosition(0)

        if self.model.arc_length:
            self.arc_length_input.setText(str(self.model.arc_length))
            self.arc_length_input.setCursorPosition(0)

        if self.model.graphics:
            items = self.model.graphics[0].plot_items()
            self.graphic.set_element(items)

    def model_loaded(self):
        self.header.blockSignals(True)
        self.fx_input.blockSignals(True)
        self.interval_a_input.blockSignals(True)
        self.interval_b_input.blockSignals(True)
        self.graphic.blockSignals(True)

        if self.model.title:
            self.header.setText(self.model.title)
        self.fx_input.setText(self.model.fx)
        self.interval_a_input.setText(str(self.model.interval[0]))
        self.interval_b_input.setText(str(self.model.interval[1]))

        self.header.blockSignals(False)
        self.fx_input.blockSignals(False)
        self.interval_a_input.blockSignals(False)
        self.interval_b_input.blockSignals(False)
        self.graphic.blockSignals(False)

        # Paint graphic
        if self.model.fx:
            self.model.set_fx(self.model.fx)

    def validation_error(self, message: str):
        self.error_label.setText(message)
        self.in_normal_state()

    def interval_input_changed(self):
        value_a = self.interval_a_input.text()
        value_b = self.interval_b_input.text()

        if not value_a or not value_b:
            self.validation_error("Введите границы трапеции")
            return

        try:
            value_a = float(value_a)
            value_b = float(value_b)
        except ValueError:
            self.validation_error("Границы должны быть числами")
            return

        self.model.set_interval((value_a, value_b))

    def limit_changed(self):
        if self.graphic.x_limits() != self.model.x_limits:
            self.model.set_x_limits(self.graphic.x_limits())
        if self.graphic.y_limits() != self.model.y_limits:
            self.model.set_y_limits(self.graphic.y_limits())

    def calc_button_clicked(self):
        self.in_progress_state()
        self.model.calc()

    def in_progress_state(self):
        self.calc_button.setDisabled(True)
        self.fx_input.setDisabled(True)
        self.interval_a_input.setDisabled(True)
        self.interval_b_input.setDisabled(True)

    def in_normal_state(self):
        self.calc_button.setDisabled(False)
        self.fx_input.setDisabled(False)
        self.interval_a_input.setDisabled(False)
        self.interval_b_input.setDisabled(False)
