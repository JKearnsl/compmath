from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QStandardItem, QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView
)

from compmath.models.slat.base import BaseSLATModel
from compmath.views.widgets import WidgetsFactory


class SLATItemView(QWidget):
    def __init__(
            self,
            model: BaseSLATModel,
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
        bottom.setContentsMargins(0, 10, 0, 10)
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
        layout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignCenter)

        matrix = widgets_factory.matrix()
        self.matrix = matrix
        left.addWidget(matrix)

        x0 = widgets_factory.matrix()
        x0.is_hidden_b = True
        x0.setFixedHeight(30)

        self.x0 = x0
        left.addWidget(x0)

        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        right.setAlignment(Qt.AlignmentFlag.AlignTop)
        right.setSpacing(10)
        bottom.addLayout(right)

        size_layout = QHBoxLayout()
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_label = widgets_factory.label("Размер: ")
        size_input = widgets_factory.spin_box()
        size_input.setMaximumWidth(100)
        size_layout.addWidget(size_label)
        size_layout.addWidget(size_input, alignment=Qt.AlignmentFlag.AlignLeft)
        self.size_input = size_input
        right.addLayout(size_layout)

        iters_limit_label = widgets_factory.label("Max итераций: ")
        iters_limit_input = widgets_factory.line_edit()
        iters_limit_input.setValidator(QIntValidator())
        self.iters_limit_input = iters_limit_input
        iters_limit_input.setMaximumWidth(100)
        iters_limit_layout = QHBoxLayout()
        iters_limit_layout.setContentsMargins(0, 0, 0, 0)
        iters_limit_layout.addWidget(iters_limit_label)
        iters_limit_layout.addWidget(iters_limit_input, alignment=Qt.AlignmentFlag.AlignLeft)
        right.addLayout(iters_limit_layout)

        eps_layout = QHBoxLayout()
        eps_layout.setContentsMargins(0, 0, 0, 0)
        eps_label = widgets_factory.label("Точность: ")
        eps_input = widgets_factory.line_edit()
        eps_input.setMaximumWidth(100)
        eps_input.setValidator(QDoubleValidator())
        eps_layout.addWidget(eps_label)
        eps_layout.addWidget(eps_input, alignment=Qt.AlignmentFlag.AlignLeft)
        self.eps_input = eps_input
        right.addLayout(eps_layout)

        calc_button = widgets_factory.button("Рассчитать")
        calc_button.setMaximumWidth(150)
        calc_button.setMinimumWidth(100)
        right.addWidget(calc_button)
        self.calc_button = calc_button

        result_button = widgets_factory.button("Результат")
        result_button.setMaximumWidth(150)
        result_button.setMinimumWidth(100)
        result_button.setDisabled(True)
        right.addWidget(result_button)
        self.result_button = result_button

        # События
        size_input.valueChanged.connect(self.size_changed)
        eps_input.textChanged.connect(self.eps_changed)
        result_button.clicked.connect(self.show_result)
        calc_button.clicked.connect(self.model.calc)
        matrix.itemChanged.connect(self.item_changed)
        x0.itemChanged.connect(self.item_x0_changed)
        iters_limit_input.textChanged.connect(self.iters_limit_changed)

    def model_changed(self):
        self.error_label.setText("")

        self.matrix.blockSignals(True)
        self.matrix.set_a(self.model.a())
        self.matrix.set_b(self.model.b())
        self.matrix.blockSignals(False)

        self.x0.blockSignals(True)
        self.x0.set_a([self.model.x0])
        self.x0.blockSignals(False)

    def was_calculated(self):
        if self.model.table:
            self.result_button.setDisabled(False)

    def model_loaded(self):
        self.header.blockSignals(True)
        self.description.blockSignals(True)
        self.eps_input.blockSignals(True)
        self.matrix.blockSignals(True)
        self.x0.blockSignals(True)
        self.iters_limit_input.blockSignals(True)

        self.header.setText(self.model.title)
        self.description.setText(self.model.description)
        self.eps_input.setText(str(self.model.eps))
        self.matrix.set_a(self.model.a())
        self.matrix.set_b(self.model.b())
        self.x0.set_a([self.model.x0])
        self.iters_limit_input.setText(str(self.model.iters_limit))

        self.header.blockSignals(False)
        self.description.blockSignals(False)
        self.eps_input.blockSignals(False)
        self.matrix.blockSignals(False)
        self.x0.blockSignals(False)
        self.iters_limit_input.blockSignals(False)
        self.size_input.blockSignals(False)

        self.size_input.setRange(3, 8)
        model_size = self.model.size()
        self.size_input.setValue(4)  # TODO: fix this bug
        if model_size:
            self.size_input.setValue(model_size)

    def validation_error(self, message: str):
        self.error_label.setText(message)

    def error_handler(self, error):
        self.error_label.setText(error)

    def size_changed(self):
        value = self.size_input.value()
        if value is None:
            return
        self.model.resize(value)

    def eps_changed(self):
        value = self.eps_input.text()
        if not value:
            return

        try:
            value = float(value)
        except ValueError:
            return

        self.model.set_eps(value)

    def item_changed(self, event: QStandardItem):
        item = event.index()
        row_index = item.row()
        column_index = item.column()
        value = event.text()
        try:
            value = float(value)
        except ValueError:
            value = 0
        self.model.set_item_value(row_index, column_index, value)

    def item_x0_changed(self, event: QStandardItem):
        item = event.index()
        index = item.column()
        value = event.text()
        try:
            value = float(value)
        except ValueError:
            value = 0
        self.model.set_item_x0_value(index, value)

    def show_result(self):
        modal = self.widgets_factory.modal(self.parent)
        modal.setFixedWidth(800)
        modal.setFixedHeight(450)
        modal.layout().setContentsMargins(5, 0, 5, 5)
        table = self.widgets_factory.table()
        table.setFixedHeight(400)
        table.setRowCount(len(self.model.table))
        table.add_style("""
            QTableWidget {
                border: none;
            }
            """)
        table.setColumnCount(len(self.model.x0) + 2)
        table.setHorizontalHeaderLabels([
            "№",
            "delta",
            *[f"x{i}" for i in range(len(self.model.x0))]
        ])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for i, row in enumerate(self.model.table):
            table.setItem(i, 0, QTableWidgetItem(str(row.iter_num)))
            table.setItem(i, 1, QTableWidgetItem(str(row.delta)))
            for j, x in enumerate(row.vector):
                table.setItem(i, j + 2, QTableWidgetItem(str(x)))
        modal.layout().addWidget(table)
        modal.exec()

    def iters_limit_changed(self):
        value = self.iters_limit_input.text()
        if not value:
            return

        try:
            value = int(value)
        except ValueError:
            return

        self.model.set_iters_limit(value)
