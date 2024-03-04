from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QTableWidgetItem, QHeaderView
)

from compmath.models.nonlinear.base import BaseNoNLinearModel
from compmath.views.widgets import WidgetsFactory


class NoNLinearItemView(QWidget):
    def __init__(
            self,
            model: BaseNoNLinearModel,
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
        layout.setSpacing(25)

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

        bottom = QHBoxLayout()
        bottom.setContentsMargins(10, 10, 10, 10)
        bottom.setSpacing(20)
        layout.addLayout(bottom)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setAlignment(Qt.AlignmentFlag.AlignTop)
        left.setSpacing(20)
        bottom.addLayout(left)

        error_label = widgets_factory.label()
        error_label.setWordWrap(True)
        error_label.setTextFormat(Qt.TextFormat.RichText)
        error_label.setFixedHeight(20)
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
        left.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignCenter)

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

        eps_label = widgets_factory.label("Точность: ")
        eps_input = widgets_factory.line_edit()
        validator = QDoubleValidator()
        validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        eps_input.setValidator(validator)
        self.eps_input = eps_input
        form.addRow(eps_label, eps_input)

        interval_a_label = widgets_factory.label("a = ")
        interval_a_input = widgets_factory.line_edit()
        interval_a_input.setValidator(QDoubleValidator())
        self.interval_a_input = interval_a_input
        form.addRow(interval_a_label, interval_a_input)

        interval_b_label = widgets_factory.label("b = ")
        interval_b_input = widgets_factory.line_edit()
        interval_b_input.setValidator(QDoubleValidator())
        self.interval_b_input = interval_b_input
        form.addRow(interval_b_label, interval_b_input)

        iters_limit_label = widgets_factory.label("Лимит итераций: ")
        iters_limit_input = widgets_factory.line_edit()
        iters_limit_input.setValidator(QIntValidator())
        self.iters_limit_input = iters_limit_input
        form.addRow(iters_limit_label, iters_limit_input)

        count_iters_label = widgets_factory.label("Кол-во итераций: ")
        count_iters_input = widgets_factory.line_edit()
        count_iters_input.setReadOnly(True)
        self.count_iters_input = count_iters_input
        form.addRow(count_iters_label, count_iters_input)

        result_label = widgets_factory.label("Результат: ")
        result_input = widgets_factory.line_edit()
        result_input.setReadOnly(True)
        self.result_input = result_input
        form.addRow(result_label, result_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.setSpacing(10)
        left.addLayout(buttons_layout)

        table_button = widgets_factory.button("Таблица")
        table_button.setMaximumWidth(150)
        table_button.setMinimumWidth(100)
        table_button.setDisabled(True)
        buttons_layout.addWidget(table_button)
        self.table_button = table_button

        calc_button = widgets_factory.button("Рассчитать")
        calc_button.setMaximumWidth(150)
        calc_button.setMinimumWidth(100)
        buttons_layout.addWidget(calc_button)
        self.calc_button = calc_button

        graphic = widgets_factory.graphic()
        graphic.setFixedWidth(350)
        graphic.setFixedHeight(350)
        self.graphic = graphic
        bottom.addWidget(graphic)

        # События
        fx_input.textChanged.connect(self.model.set_fx)
        eps_input.textChanged.connect(self.eps_changed)
        interval_a_input.textChanged.connect(self.interval_input_changed)
        interval_b_input.textChanged.connect(self.interval_input_changed)
        iters_limit_input.textChanged.connect(self.iters_limit_changed)
        graphic.limitChanged.connect(self.limit_changed)
        table_button.clicked.connect(self.show_table)
        calc_button.clicked.connect(self.model.calc)

    def model_changed(self):
        self.error_label.setText("")

        if self.model.iters is not None:
            self.count_iters_input.setText(str(self.model.iters))

        if self.model.result is not None:
            self.result_input.setText(str(self.model.result))
            self.result_input.setCursorPosition(0)

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
        self.eps_input.blockSignals(True)
        self.interval_a_input.blockSignals(True)
        self.interval_b_input.blockSignals(True)
        self.graphic.blockSignals(True)
        self.iters_limit_input.blockSignals(True)

        self.header.setText(self.model.title)
        self.description.setText(self.model.description)
        self.fx_input.setText(self.model.fx)
        self.eps_input.setText(str(self.model.eps))
        self.interval_a_input.setText(str(self.model.interval[0]))
        self.interval_b_input.setText(str(self.model.interval[1]))
        self.graphic.set_x_limits(self.model.x_limits)
        self.graphic.set_y_limits(self.model.y_limits)
        self.iters_limit_input.setText(str(self.model.iters_limit))

        self.header.blockSignals(False)
        self.description.blockSignals(False)
        self.fx_input.blockSignals(False)
        self.eps_input.blockSignals(False)
        self.interval_a_input.blockSignals(False)
        self.interval_b_input.blockSignals(False)
        self.graphic.blockSignals(False)
        self.iters_limit_input.blockSignals(False)

        # Paint graphic
        if self.model.fx:
            self.model.set_fx(self.model.fx)

    def validation_error(self, message: str):
        self.error_label.setText(message)

    def interval_input_changed(self):
        value_a = self.interval_a_input.text()
        value_b = self.interval_b_input.text()

        if not value_a or not value_b:
            return

        try:
            value_a = float(value_a)
            value_b = float(value_b)
        except ValueError:
            return

        self.model.set_interval((value_a, value_b))

    def eps_changed(self):
        value = self.eps_input.text()
        if not value:
            return

        try:
            value = float(value)
        except ValueError:
            return

        self.model.set_eps(value)

    def limit_changed(self):
        if self.graphic.x_limits() != self.model.x_limits:
            self.model.set_x_limits(self.graphic.x_limits())
            self.model.reset_graphic()
        if self.graphic.y_limits() != self.model.y_limits:
            self.model.set_y_limits(self.graphic.y_limits())
            self.model.reset_graphic()

    def iters_limit_changed(self):
        value = self.iters_limit_input.text()
        if not value:
            return

        try:
            value = int(value)
        except ValueError:
            return

        self.model.set_iters_limit(value)

    def show_table(self):
        modal = self.widgets_factory.modal(self.parent)
        modal.setFixedWidth(800)
        modal.setFixedHeight(450)
        modal.layout().setContentsMargins(5, 0, 5, 5)
        table = self.widgets_factory.table()
        table.setFixedHeight(400)
        table.setRowCount(len(self.model.table))
        table.setColumnCount(8)
        table.add_style("""
            QTableWidget {
                border: none;
            }
            """)
        table.setHorizontalHeaderLabels([
            "№",
            "a",
            "b",
            "x",
            "f(x)",
            "f(a)",
            "f(b)",
            "|a - b|"
        ])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for i, row in enumerate(self.model.table):
            table.setItem(i, 0, QTableWidgetItem(str(row.iter_num)))
            table.setItem(i, 1, QTableWidgetItem(str(row.a)))
            table.setItem(i, 2, QTableWidgetItem(str(row.b)))
            table.setItem(i, 3, QTableWidgetItem(str(row.x)))
            table.setItem(i, 4, QTableWidgetItem(str(row.fx)))
            table.setItem(i, 5, QTableWidgetItem(str(row.fa)))
            table.setItem(i, 6, QTableWidgetItem(str(row.fb)))
            table.setItem(i, 7, QTableWidgetItem(str(row.distance)))
            table.item(i, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        modal.layout().addWidget(table)
        modal.exec()
