from PyQt6 import sip
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QTableWidgetItem
)

from compmath.models.ni.base import BaseNIModel
from compmath.views.widgets import WidgetsFactory


class NItemView(QWidget):
    def __init__(
            self,
            model: BaseNIModel,
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

        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)
        layout.addLayout(info_layout)

        header = widgets_factory.heading4("None")
        info_layout.addWidget(header)
        self.header = header

        description = widgets_factory.label()
        description.setWordWrap(True)
        description.setTextFormat(Qt.TextFormat.RichText)
        description.setText("None")
        description.setMaximumWidth(600)
        description.setMinimumWidth(400)
        info_layout.addWidget(description)
        self.description = description

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

        intervals_label = widgets_factory.label("Интервалов: ")
        intervals_input = widgets_factory.line_edit()
        intervals_input.setValidator(QIntValidator(bottom=1))
        self.intervals_input = intervals_input
        form.addRow(intervals_label, intervals_input)

        result_label = widgets_factory.label("Результат: ")
        result_input = widgets_factory.line_edit()
        result_input.setReadOnly(True)
        self.result_input = result_input
        form.addRow(result_label, result_input)

        abs_delta_label = widgets_factory.label("Абсолютная Δ: ")
        abs_delta_input = widgets_factory.line_edit()
        abs_delta_input.setReadOnly(True)
        self.abs_delta_input = abs_delta_input
        form.addRow(abs_delta_label, abs_delta_input)

        relative_delta_label = widgets_factory.label("Относительная Δ: ")
        relative_delta_input = widgets_factory.line_edit()
        relative_delta_input.setReadOnly(True)
        self.relative_delta_input = relative_delta_input
        form.addRow(relative_delta_label, relative_delta_input)

        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.setSpacing(10)
        left.addLayout(buttons_layout)

        calc_button = widgets_factory.button("Рассчитать")
        calc_button.setMaximumWidth(200)
        calc_button.setMinimumWidth(180)
        buttons_layout.addWidget(calc_button)
        self.calc_button = calc_button

        table_button = widgets_factory.button("Таблица")
        table_button.setMaximumWidth(200)
        table_button.setMinimumWidth(180)
        table_button.setDisabled(True)
        buttons_layout.addWidget(table_button)
        self.table_button = table_button

        graphic = widgets_factory.graphic()
        graphic.setFixedWidth(350)
        graphic.setFixedHeight(350)
        graphic.setSliderEnabled(False)
        self.graphic = graphic
        bottom.addWidget(graphic)

        self.background_jobs = []

        # События
        fx_input.textChanged.connect(lambda text: self.model.set_fx(text))
        intervals_input.textChanged.connect(self.intervals_changed)
        interval_a_input.textChanged.connect(self.interval_input_changed)
        interval_b_input.textChanged.connect(self.interval_input_changed)
        graphic.limitChanged.connect(self.limit_changed)
        table_button.clicked.connect(self.show_table)
        calc_button.clicked.connect(self.calc_button_clicked)

    def model_changed(self):
        if not self and sip.isdeleted(self):
            return

        self.error_label.setText("")

        if self.model.result is not None:
            self.result_input.setText(str(self.model.result))
            self.in_calc_state()
            self.result_input.setCursorPosition(0)

        if self.model.abs_delta is not None:
            abs_delta = format(self.model.abs_delta, ".17f")
            if '.' in abs_delta:
                abs_delta = abs_delta.rstrip('0').rstrip('.')
            self.abs_delta_input.setText(abs_delta)
            self.abs_delta_input.setCursorPosition(0)

        if self.model.relative_delta is not None:
            relative_delta = format(self.model.relative_delta, ".17f")
            if '.' in relative_delta:
                relative_delta = relative_delta.rstrip('0').rstrip('.')
            self.relative_delta_input.setText(relative_delta)
            self.relative_delta_input.setCursorPosition(0)

        if self.model.table:
            self.table_button.setDisabled(False)

        if self.model.graphics:
            self.graphic.clear_plots()
            for plot in self.model.graphics:
                self.graphic.add_plot(plot.plot_items())

    def model_loaded(self):
        self.header.blockSignals(True)
        self.description.blockSignals(True)
        self.fx_input.blockSignals(True)
        self.intervals_input.blockSignals(True)
        self.interval_a_input.blockSignals(True)
        self.interval_b_input.blockSignals(True)
        self.graphic.blockSignals(True)

        self.header.setText(self.model.title)
        self.description.setText(self.model.description)
        self.fx_input.setText(self.model.fx)
        self.intervals_input.setText(str(self.model.intervals))
        self.interval_a_input.setText(str(self.model.interval[0]))
        self.interval_b_input.setText(str(self.model.interval[1]))
        self.graphic.set_x_limits(self.model.x_limits)
        self.graphic.set_y_limits(self.model.y_limits)

        self.header.blockSignals(False)
        self.description.blockSignals(False)
        self.fx_input.blockSignals(False)
        self.intervals_input.blockSignals(False)
        self.interval_a_input.blockSignals(False)
        self.interval_b_input.blockSignals(False)
        self.graphic.blockSignals(False)

        # Paint graphic
        if self.model.fx:
            self.model.set_fx(self.model.fx)

    def validation_error(self, message: str):
        self.error_label.setText(message)

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
            self.model.reset_graphic()
        if self.graphic.y_limits() != self.model.y_limits:
            self.model.set_y_limits(self.graphic.y_limits())
            self.model.reset_graphic()

    def intervals_changed(self):
        value = self.intervals_input.text()
        if not value:
            self.validation_error("Введите количество интервалов")
            return

        try:
            value = int(value)
        except ValueError:
            self.validation_error("Количество интервалов должно быть целым числом")
            return

        self.model.set_intervals(value)

    def calc_button_clicked(self):
        self.in_progress_state()
        self.model.calc()

    def in_progress_state(self):
        self.calc_button.setDisabled(True)
        self.fx_input.setDisabled(True)
        self.intervals_input.setDisabled(True)
        self.interval_a_input.setDisabled(True)
        self.interval_b_input.setDisabled(True)

    def in_calc_state(self):
        self.calc_button.setDisabled(False)
        self.fx_input.setDisabled(False)
        self.intervals_input.setDisabled(False)
        self.interval_a_input.setDisabled(False)
        self.interval_b_input.setDisabled(False)

    def show_table(self):
        modal = self.widgets_factory.modal(self.parent)
        modal.setFixedWidth(800)
        modal.setFixedHeight(450)
        modal.layout().setContentsMargins(5, 0, 5, 5)
        table = self.widgets_factory.table()
        table.setFixedHeight(400)
        table.setRowCount(len(self.model.table))
        table.setColumnCount(4)
        table.add_style(""" QTableWidget { border: none; } """)
        table.setHorizontalHeaderLabels(["№", "x", "y", "Интеграл"])
        for i, row in enumerate(self.model.table):
            table.setItem(i, 0, QTableWidgetItem(str(row.num)))
            table.setItem(i, 1, QTableWidgetItem(str(row.x)))
            table.setItem(i, 2, QTableWidgetItem(str(row.y)))
            table.setItem(i, 3, QTableWidgetItem(str(row.value)))
        modal.layout().addWidget(table)
        modal.exec()
