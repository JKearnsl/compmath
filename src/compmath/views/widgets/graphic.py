import logging

from PyQt6 import sip
from PyQt6.QtCore import QPointF, Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QToolButton,
    QVBoxLayout,
    QSlider
)

from pyqtgraph import PlotDataItem, AxisItem
from pyqtgraph import PlotWidget, InfiniteLine

from compmath.utils.icon import svg_ico
from compmath.views.widgets import Dialog
from compmath.views.widgets.input_label import InputLabel


class GraphicCanvas(PlotWidget):
    def __init__(self, background_color: str = "white", axis_color: str = "black", parent=None):
        self.axis_x = AxisItem(orientation='bottom')
        self.axis_y = AxisItem(orientation='left')
        super().__init__(
            parent,
            background=background_color,
            axisItems={'bottom': self.axis_x, 'left': self.axis_y}
        )
        self._temp_items = []

        # Создание линий, которые будут служить осями
        x_axis_line = InfiniteLine(pos=0, angle=0, movable=False, pen=axis_color)
        y_axis_line = InfiniteLine(pos=0, angle=90, movable=False, pen=axis_color)

        self.addItem(x_axis_line)
        self.addItem(y_axis_line)

        self.showGrid(x=True, y=True)
        self.setBackground(background_color)

    def add_temp_item(self, item: PlotDataItem):
        if self and not sip.isdeleted(self):
            self._temp_items.append(item)
            self.addItem(item)
        else:
            logging.warning("[GraphicWidget] is deleted")

    def clear_temp_items(self):
        if self and not sip.isdeleted(self):
            for item in self._temp_items:
                self.removeItem(item)
            self._temp_items.clear()
        else:
            logging.warning("GraphicWidget is deleted")

    def temp_items(self) -> list[PlotDataItem]:
        return self._temp_items


def copy_plot_data_item(item: PlotDataItem) -> PlotDataItem:
    x, y = item.getData()

    copied_item = PlotDataItem(x, y)

    copied_item.setPen(item.opts['pen'])
    copied_item.setSymbol(item.opts['symbol'])
    copied_item.setSymbolBrush(item.opts['symbolBrush'])
    copied_item.setSymbolPen(item.opts['symbolPen'])

    return copied_item


class Graphic(QWidget):
    limitInvalid = pyqtSignal()
    limitChanged = pyqtSignal()

    def __init__(
            self,
            text_color: str,
            hover_color: str,
            background_color: str,
            dialog_background_color: str,
            text_header_color: str,
            parent: QWidget = None
    ):
        super().__init__(parent)

        self._plots: list[list[PlotDataItem]] = []
        self._current_plot = None
        self._slider_enabled = True

        self._text_color = text_color
        self._text_header_color = text_header_color
        self._hover_color = hover_color
        self._dialog_background_color = dialog_background_color
        self._background_color = background_color

        widget_layout = QVBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)
        self.setLayout(widget_layout)

        sheet = QWidget(self)
        sheet.setObjectName("sheet")
        widget_layout.addWidget(sheet)
        sheet.setStyleSheet("""
            QWidget#sheet {
                border: none;
                border-radius: 5px;
            }
        """.replace(
            "$HOVER", hover_color,
        ))
        sheet.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QColor(0, 0, 0, 50),
            offset=QPointF(0, 0)
        ))

        layout = QGridLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(0)
        sheet.setLayout(layout)

        x_limits_layout = QHBoxLayout()

        x_min = InputLabel(text_color)
        x_min.setFixedWidth(30)
        x_min.setFixedHeight(30)
        x_min.setText("-10")
        x_limits_layout.addWidget(x_min)
        self._x_min = x_min

        x_limits_layout.addStretch(1)

        x_max = InputLabel(text_color)
        x_max.setFixedWidth(30)
        x_max.setFixedHeight(30)
        x_max.setText("10")
        x_limits_layout.addWidget(x_max)
        self._x_max = x_max

        y_limits_layout = QVBoxLayout()

        y_max = InputLabel(text_color)
        y_max.setFixedWidth(30)
        y_max.setFixedHeight(30)
        y_max.setText("10")
        y_limits_layout.addWidget(y_max)
        self._y_max = y_max

        y_limits_layout.addStretch(1)

        y_min = InputLabel(text_color)
        y_min.setFixedWidth(30)
        y_min.setFixedHeight(30)
        y_min.setText("-10")
        y_limits_layout.addWidget(y_min)
        self._y_min = y_min

        graphic = GraphicCanvas(dialog_background_color, text_color)
        self._graphic = graphic

        toolbar = QWidget()
        toolbar.setFixedWidth(30)
        toolbar_layout = QVBoxLayout()
        toolbar.setLayout(toolbar_layout)
        toolbar_layout.setContentsMargins(0, 5, 0, 5)
        toolbar_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        toolbar_layout.setSpacing(10)

        # Fullscreen button
        fullscreen_btn = QToolButton()
        fullscreen_btn.setFixedSize(24, 24)
        fullscreen_btn.setStyleSheet("""
            QToolButton {
                border: none;
                border-radius: 5px;
                background-color: transparent;
            }
            
            QToolButton:hover {
                background-color: $HOVER;
            }
            
            QToolButton:pressed {
                background-color: transparent;
            }
            
        """.replace(
            "$HOVER", hover_color,
        ))

        fullscreen_btn.setIconSize(fullscreen_btn.size())
        fullscreen_btn.setIcon(svg_ico("icons:fullscreen.svg"))
        toolbar_layout.addWidget(fullscreen_btn)
        self.toolbar = toolbar

        graphic_slider = QSlider(Qt.Orientation.Horizontal)
        graphic_slider.setFixedHeight(20)
        graphic_slider.setFixedWidth(200)
        graphic_slider.setRange(0, 0)
        graphic_slider.setDisabled(True)
        graphic_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.graphic_slider = graphic_slider

        layout.addLayout(y_limits_layout, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(graphic, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(toolbar, 1, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        layout.addLayout(x_limits_layout, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(graphic_slider, 3, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        x_max.finishEditing.connect(self.limit_changed)
        x_min.finishEditing.connect(self.limit_changed)
        y_max.finishEditing.connect(self.limit_changed)
        y_min.finishEditing.connect(self.limit_changed)
        fullscreen_btn.clicked.connect(self.show_full_screen)
        graphic_slider.valueChanged.connect(self.set_plot)

    def x_limits(self) -> tuple[float, float]:
        return float(self._x_min.text()), float(self._x_max.text())

    def y_limits(self) -> tuple[float, float]:
        return float(self._y_min.text()), float(self._y_max.text())

    def limit_changed(self):
        x_max = self._x_max.text()
        x_min = self._x_min.text()
        y_max = self._y_max.text()
        y_min = self._y_min.text()

        if not x_max or not x_min or not y_max or not y_min:
            self.limitInvalid.emit()
            return

        try:
            float(x_max)
            float(x_min)
            float(y_max)
            float(y_min)
        except ValueError:
            self.limitInvalid.emit()
            return

        self.limitChanged.emit()

    def set_x_limits(self, x_limits: tuple[float, float]):
        self._x_max.setText(str(x_limits[1]))
        self._x_min.setText(str(x_limits[0]))

    def set_y_limits(self, y_limits: tuple[float, float]):
        self._y_max.setText(str(y_limits[1]))
        self._y_min.setText(str(y_limits[0]))

    def add_plot(self, plot_items: list[PlotDataItem]):
        self._plots.append(plot_items)
        if self._slider_enabled:
            if self.graphic_slider and not sip.isdeleted(self):
                self.graphic_slider.setEnabled(True)
                self.graphic_slider.setMaximum(len(self._plots) - 1)
                self.graphic_slider.setValue(len(self._plots) - 1)
            else:
                logging.error("[GraphicWidget] GraphicSlider is deleted")
        self.set_plot(len(self._plots) - 1)

    def set_plot(self, index: int):
        self._current_plot = index
        self._graphic.clear_temp_items()
        for item in self._plots[index]:
            self._graphic.add_temp_item(item)

    def clear_plots(self):
        self._plots.clear()
        self._current_plot = None
        self._graphic.clear_temp_items()
        self.graphic_slider.setDisabled(True)

    def show_full_screen(self):
        dialog = Dialog(
            background_window=self._dialog_background_color,
            background_close_btn=self._background_color,
            hover_close_btn=self._hover_color,
            text_color_close_btn=self._text_header_color,
            parent=self
        )
        dialog.setModal(True)
        dialog.setFixedSize(800, 450)

        graphic = GraphicCanvas(self._dialog_background_color, self._text_color)
        for item in self._graphic.temp_items():
            graphic.addItem(copy_plot_data_item(item))
        dialog.layout().addWidget(graphic)

        dialog.show()

    def setSliderEnabled(self, enabled: bool):
        self._slider_enabled = enabled
        self.graphic_slider.setVisible(enabled)
