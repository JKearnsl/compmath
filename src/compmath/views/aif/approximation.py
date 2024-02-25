from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea
)

from compmath.models.aif.base import BaseAIFModel
from compmath.views.widgets import WidgetsFactory


class AItemView(QWidget):
    def __init__(
            self,
            model: BaseAIFModel,
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
        layout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignLeft)

        bottom = QHBoxLayout()
        bottom.setContentsMargins(10, 10, 10, 10)
        bottom.setSpacing(20)
        layout.addLayout(bottom)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
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

        point_count_label = widgets_factory.label("Точек: ")
        point_count_input = widgets_factory.spin_box()
        point_count_input.setMaximumWidth(100)
        self.point_count_input = point_count_input
        form.addRow(point_count_label, point_count_input)

        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.setSpacing(10)
        left.addLayout(buttons_layout)

        calc_button = widgets_factory.button("Рассчитать")
        calc_button.setMaximumWidth(150)
        calc_button.setMinimumWidth(100)
        buttons_layout.addWidget(calc_button)
        self.calc_button = calc_button

        result_button = widgets_factory.button("Результат")
        result_button.setMaximumWidth(150)
        result_button.setMinimumWidth(100)
        result_button.setDisabled(True)
        buttons_layout.addWidget(result_button)
        self.result_button = result_button

        input_table = widgets_factory.table()
        input_table.setFixedWidth(125)
        input_table.setColumnCount(2)
        input_table.setHorizontalHeaderLabels(["X", "Y"])
        input_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        input_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        bottom.addWidget(input_table)
        self.input_table = input_table

        graphic = widgets_factory.graphic()
        graphic.setFixedWidth(325)
        graphic.setFixedHeight(350)
        self.graphic = graphic
        bottom.addWidget(graphic)

        # События
        point_count_input.valueChanged.connect(self.point_count_changed)
        input_table.cellChanged.connect(self.point_changed)
        graphic.limitChanged.connect(self.limit_changed)
        result_button.clicked.connect(self.show_result)
        calc_button.clicked.connect(self.model.calc)

    def model_changed(self):
        self.error_label.setText("")

        if self.model.results:
            self.result_button.setDisabled(False)

        if self.model.graphics:
            self.graphic.clear_plots()
            for plot in self.model.graphics:
                self.graphic.add_plot(plot.plot_items())

        self.input_table.setRowCount(len(self.model.points))
        self.input_table.blockSignals(True)
        for i, row in enumerate(self.model.points):
            item_x = self.input_table.item(i, 0)
            item_y = self.input_table.item(i, 1)
            if item_x is None:
                item = QTableWidgetItem()
                item.setText(str(row[0]))
                self.input_table.setItem(i, 0, item)
            if item_y is None:
                item = QTableWidgetItem()
                item.setText(str(row[1]))
                self.input_table.setItem(i, 1, item)
        self.input_table.blockSignals(False)

        if self.model.points:
            self.graphic.clear_plots()
            self.graphic.add_plot(self.model.graphic().plot_items())

    def model_loaded(self):
        self.header.blockSignals(True)
        self.description.blockSignals(True)
        self.graphic.blockSignals(True)

        self.header.setText(self.model.title)
        self.description.setText(self.model.description)
        self.graphic.set_x_limits(self.model.x_limits)

        self.header.blockSignals(False)
        self.description.blockSignals(False)
        self.graphic.blockSignals(False)

        self.point_count_input.blockSignals(True)
        self.point_count_input.setValue(len(self.model.points))
        self.point_count_input.blockSignals(False)

        self.model_changed()

    def validation_error(self, message: str):
        self.error_label.setText(message)

    def limit_changed(self):
        if self.graphic.x_limits() != self.model.x_limits:
            self.model.set_x_limits(self.graphic.x_limits())
        if self.graphic.y_limits() != self.model.y_limits:
            self.model.set_y_limits(self.graphic.y_limits())

    def point_count_changed(self):
        count = self.point_count_input.value()
        try:
            count = int(count)
        except ValueError:
            return
        self.model.resize(count)

    def point_changed(self, row_index: int):
        x = self.input_table.item(row_index, 0)
        y = self.input_table.item(row_index, 1)
        try:
            x_value = float(x.text())
        except (ValueError, AttributeError):
            x_value = 0
        try:
            y_value = float(y.text())
        except (ValueError, AttributeError):
            y_value = 0

        self.model.set_point(row_index, (x_value, y_value))

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

        items = list(sorted(self.model.results, key=lambda x: (abs(x[2][0]), abs(1 - x[2][1]))))

        for number, item in enumerate(self.model.results, 1):
            graphic, log, (sum_diff, coefficient), title = item

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
            if items.index(item) == 0:
                log.append(
                    "\nДанный вариант аппроксимирующей функции "
                    "наилучшим образом среди рассмотренных приближает "
                    "исходную таблично заданную функцию."
                )

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
            log_area.setFixedHeight(400)
            log_area.setReadOnly(True)
            log_area.setPlainText("\n".join(log))
            text_layout.addWidget(log_area)

            result_box = QFormLayout()
            result_box.setContentsMargins(5, 5, 5, 5)
            result_box.setSpacing(5)
            text_layout.addLayout(result_box)

            sum_diff_label = self.widgets_factory.label("Сумма квадратов разностей:")
            sum_diff_value = self.widgets_factory.line_edit()
            sum_diff_value.setReadOnly(True)
            sum_diff_value.setText(str(sum_diff))
            result_box.addRow(sum_diff_label, sum_diff_value)

            coefficient_label = self.widgets_factory.label("Коэффициент корреляции:")
            coefficient_value = self.widgets_factory.line_edit()
            coefficient_value.setReadOnly(True)
            coefficient_value.setText(str(coefficient))
            result_box.addRow(coefficient_label, coefficient_value)

            rating = self.widgets_factory.label("Рейтинг:")
            rating_value = self.widgets_factory.label(f"{len(items) - items.index(item)} из {len(items)}")
            result_box.addRow(rating, rating_value)

            graphic_widget = self.widgets_factory.graphic()
            graphic_widget.setFixedSize(QSize(300, 300))
            graphic_widget.add_plot(graphic.plot_items())
            graphic_widget.graphic_slider.setEnabled(False)
            content_layout.addWidget(graphic_widget)

        modal.exec()
