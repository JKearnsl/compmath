from typing import cast

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView, QListWidget, QListWidgetItem, QScrollArea
)

from compmath.models.sne.base import BaseSNEModel
from compmath.views.widgets import WidgetsFactory


class EquationItem(QListWidgetItem):
    def __init__(self):
        super().__init__()
        self.setSizeHint(QSize(0, 40))
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsEnabled)


class EquationItemWidget(QWidget):
    ItemChanged = pyqtSignal(int, str)

    def __init__(self, index: int, str_func: str, widgets_factory: WidgetsFactory, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        index_label = widgets_factory.label(f"[{index + 1}]")
        layout.addWidget(index_label)

        func = widgets_factory.line_edit()
        func.add_style("""
            QLineEdit {
                background-color: $BG1;
            }
        """.replace(
            "$BG1", widgets_factory.theme.first_background
        ))
        func.setText(str_func)
        layout.addWidget(func)
        self.func = func
        self.index = index

        self.func.textChanged.connect(lambda: self.ItemChanged.emit(self.index, self.func.text()))


class SNEItemView(QWidget):
    def __init__(
            self,
            model: BaseSNEModel,
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
        layout.setSpacing(10)

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
        layout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignCenter)

        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)
        bottom.setSpacing(20)
        layout.addLayout(bottom)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setAlignment(Qt.AlignmentFlag.AlignTop)
        left.setSpacing(10)
        bottom.addLayout(left)

        equation_count_layout = QHBoxLayout()
        equation_count_layout.setContentsMargins(0, 0, 0, 0)
        equation_count_label = widgets_factory.label("Уравнений: ")
        equation_count_input = widgets_factory.spin_box()
        equation_count_input.setMaximumWidth(100)
        equation_count_layout.addWidget(equation_count_label)
        equation_count_layout.addWidget(equation_count_input, alignment=Qt.AlignmentFlag.AlignLeft)
        self.equation_count_input = equation_count_input
        left.addLayout(equation_count_layout)

        initial_guess_layout = QHBoxLayout()
        initial_guess_layout.setContentsMargins(0, 0, 0, 0)
        initial_guess_label = widgets_factory.label("Нач. прибл.: ")
        initial_guess_input = widgets_factory.line_edit()
        initial_guess_input.setMaximumWidth(100)
        initial_guess_layout.addWidget(initial_guess_label)
        initial_guess_layout.addWidget(initial_guess_input, alignment=Qt.AlignmentFlag.AlignLeft)
        self.initial_guess_input = initial_guess_input
        left.addLayout(initial_guess_layout)

        iters_limit_label = widgets_factory.label("Max итераций: ")
        iters_limit_input = widgets_factory.line_edit()
        iters_limit_input.setValidator(QIntValidator())
        self.iters_limit_input = iters_limit_input
        iters_limit_input.setMaximumWidth(100)
        iters_limit_layout = QHBoxLayout()
        iters_limit_layout.setContentsMargins(0, 0, 0, 0)
        iters_limit_layout.addWidget(iters_limit_label)
        iters_limit_layout.addWidget(iters_limit_input, alignment=Qt.AlignmentFlag.AlignLeft)
        left.addLayout(iters_limit_layout)

        eps_layout = QHBoxLayout()
        eps_layout.setContentsMargins(0, 0, 0, 0)
        eps_label = widgets_factory.label("Точность: ")
        eps_input = widgets_factory.line_edit()
        eps_input.setMaximumWidth(100)
        eps_input.setValidator(QDoubleValidator())
        eps_layout.addWidget(eps_label)
        eps_layout.addWidget(eps_input, alignment=Qt.AlignmentFlag.AlignLeft)
        self.eps_input = eps_input
        left.addLayout(eps_layout)

        calc_button = widgets_factory.button("Рассчитать")
        calc_button.setMaximumWidth(150)
        calc_button.setMinimumWidth(100)
        left.addWidget(calc_button)
        self.calc_button = calc_button

        result_button = widgets_factory.button("Результат")
        result_button.setMaximumWidth(150)
        result_button.setMinimumWidth(100)
        result_button.setDisabled(True)
        left.addWidget(result_button)
        self.result_button = result_button

        graphic = widgets_factory.graphic()
        graphic.graphic_slider.setVisible(False)
        graphic.setFixedSize(QSize(250, 200))
        self.graphic = graphic
        bottom.addWidget(graphic)

        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        right.setAlignment(Qt.AlignmentFlag.AlignTop)
        right.setSpacing(20)
        bottom.addLayout(right)

        equation_list = QListWidget()
        equation_list.setObjectName("equation_list")
        equation_list.setStyleSheet("""
                    QListWidget#equation_list {
                        background-color: $BG2;
                        border-radius: 5px;
                        border: 2px solid $HOVER;
                    }
                """.replace(
            "$BG2", widgets_factory.theme.second_background
        ).replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        self.equation_list = equation_list
        right.addWidget(equation_list)

        # События
        initial_guess_input.textChanged.connect(self.initial_guess_changed)
        equation_count_input.valueChanged.connect(self.model.set_equation_count)
        eps_input.textChanged.connect(self.eps_changed)
        result_button.clicked.connect(self.show_result)
        calc_button.clicked.connect(self.model.calc)
        iters_limit_input.textChanged.connect(self.iters_limit_changed)

    def model_changed(self):
        self.error_label.setText("")

        if self.model.table:
            self.result_button.setDisabled(False)

        if self.model.equations:
            self.graphic.clear_plots()
            self.graphic.add_plot(
                self.model.graphic(self.graphic.x_limits()).plot_items()
            )

        if self.equation_list.count() > len(self.model.equations):
            for i in range(len(self.model.equations), self.equation_list.count()):
                self.equation_list.takeItem(i)

        for index, str_func in enumerate(self.model.equations):
            item = self.equation_list.item(index)
            if item is not None:
                widget = self.equation_list.itemWidget(item)
                if widget.func.text() != str_func:
                    widget.func.setText(str_func)
            else:
                new_item = EquationItem()
                new_widget = EquationItemWidget(index, str_func, self.widgets_factory)
                new_widget.ItemChanged.connect(self.item_changed)
                self.equation_list.addItem(new_item)
                self.equation_list.setItemWidget(new_item, new_widget)

    def model_loaded(self):
        self.header.blockSignals(True)
        self.description.blockSignals(True)
        self.eps_input.blockSignals(True)
        self.iters_limit_input.blockSignals(True)
        self.initial_guess_input.blockSignals(True)

        self.header.setText(self.model.title)
        self.description.setText(self.model.description)
        self.eps_input.setText(str(self.model.eps))
        self.iters_limit_input.setText(str(self.model.iters_limit))
        self.initial_guess_input.setText(f"{self.model.initial_guess[0]}, {self.model.initial_guess[1]}")

        self.header.blockSignals(False)
        self.description.blockSignals(False)
        self.eps_input.blockSignals(False)
        self.iters_limit_input.blockSignals(False)
        self.initial_guess_input.blockSignals(False)

        self.equation_count_input.setRange(2, 10)
        self.equation_count_input.setEnabled(False)
        self.equation_count_input.setValue(2)

    def validation_error(self, message: str):
        self.error_label.setText(message)

    def error_handler(self, error):
        self.error_label.setText(error)

    def initial_guess_changed(self):
        value = self.initial_guess_input.text()
        if value is None:
            return

        try:
            value = tuple(map(float, value.strip().split(',')))
            if len(value) != 2:
                raise ValueError
        except ValueError:
            return

        self.model.set_initial_guess(cast(tuple[int | float, int | float], value))

    def eps_changed(self):
        value = self.eps_input.text()
        if not value:
            return

        try:
            value = float(value)
        except ValueError:
            return

        self.model.set_eps(value)

    def item_changed(self, index: int, value: str):
        if value.strip() == "":
            return
        self.model.set_equation(index, value)

    def show_result(self):
        modal = self.widgets_factory.modal(self.parent)
        modal.setFixedWidth(800)
        modal.setFixedHeight(450)
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
        scroll_area.setObjectName("scroll_area")
        scroll_area.setStyleSheet("""
            QWidget#scroll_area {
                border: none;
                outline: none;
            }
        """)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(sheet)
        modal.layout().addWidget(scroll_area)

        if self.model.solve_log:
            text_area = self.widgets_factory.textarea()
            text_area.setFixedHeight(400)
            text_area.setReadOnly(True)
            text_area.setPlainText("\n".join(self.model.solve_log))
            central_layout.addWidget(text_area)

        if self.model.table:
            table = self.widgets_factory.table()
            table.setFixedHeight(400)
            table.setRowCount(len(self.model.table))
            table.add_style("""
                QTableWidget {
                    border: none;
                }
                """)
            table.setColumnCount(len(self.model.equations) + 2)
            table.setHorizontalHeaderLabels([
                "№",
                "delta",
                *[f"a{i}" for i in range(len(self.model.equations))]
            ])
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            for i, row in enumerate(self.model.table):
                table.setItem(i, 0, QTableWidgetItem(str(row.iter_num)))
                table.setItem(i, 1, QTableWidgetItem(str(row.delta)))
                for j, x in enumerate(row.vector):
                    table.setItem(i, j + 2, QTableWidgetItem(str(x)))
            central_layout.addWidget(table)
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

    def set_equation_count(self, value: int):
        self.model.set_equation_count(value)
