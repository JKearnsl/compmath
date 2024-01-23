from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QStandardItem
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem
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
        size_input.setValue(0)
        size_input.setRange(0, 100)
        size_layout.addWidget(size_label)
        size_layout.addWidget(size_input, alignment=Qt.AlignmentFlag.AlignLeft)
        self.size_input = size_input
        right.addLayout(size_layout)

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
        result_button.clicked.connect(self.show_matrix)
        calc_button.clicked.connect(self.model.calc)
        matrix.itemChanged.connect(self.item_changed)

    def model_changed(self):
        self.error_label.setText("")

        self.matrix.blockSignals(True)
        self.matrix.set_a(self.model.a())
        self.matrix.set_b(self.model.b())
        print(self.model.matrix)
        self.matrix.blockSignals(False)

    def was_calculated(self):
        if self.model.matrix:
            self.result_button.setDisabled(False)

    def model_loaded(self):
        self.header.blockSignals(True)
        self.description.blockSignals(True)
        self.eps_input.blockSignals(True)
        self.matrix.blockSignals(True)

        self.header.setText(self.model.title)
        self.description.setText(self.model.description)
        self.eps_input.setText(str(self.model.eps))
        self.matrix.set_a(self.model.a())
        self.matrix.set_b(self.model.b())

        self.header.blockSignals(False)
        self.description.blockSignals(False)
        self.eps_input.blockSignals(False)
        self.matrix.blockSignals(False)

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
        if not value.replace("-", "").isdigit():
            value = 0
        else:
            value = float(value)
        self.model.set_item_value(row_index, column_index, value)


    def show_matrix(self):
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
        for i, row in enumerate(self.model.table):
            table.setItem(i, 0, QTableWidgetItem(str(row.iter_num)))
            table.setItem(i, 1, QTableWidgetItem(str(row.a)))
            table.setItem(i, 2, QTableWidgetItem(str(row.b)))
            table.setItem(i, 3, QTableWidgetItem(str(row.x)))
            table.setItem(i, 4, QTableWidgetItem(str(row.fx)))
            table.setItem(i, 5, QTableWidgetItem(str(row.fa)))
            table.setItem(i, 6, QTableWidgetItem(str(row.fb)))
            table.setItem(i, 7, QTableWidgetItem(str(row.distance)))
        modal.layout().addWidget(table)
        modal.exec()