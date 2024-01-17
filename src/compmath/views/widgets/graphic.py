from PyQt6.QtCore import QPointF, Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QGraphicsDropShadowEffect
from matplotlib import ticker
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

from compmath.views.widgets.input_label import InputLabel


class Canvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        fig = Figure()
        self.ax = fig.add_subplot(111)
        # установка положения осей координат
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')

        self.ax.set_xlabel(r'x', fontsize=15, loc='right')
        self.ax.set_ylabel(r'y', fontsize=15, loc='top')

        self.ax.autoscale_view()

        # Настройка сетки
        self.ax.minorticks_on()

        self.ax.grid(which='major')
        self.ax.grid(which='minor', linestyle=':')

        # self.ax.set_xlim(-10, 10)
        # self.ax.set_ylim(-10, 10)

        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        super(Canvas, self).__init__(fig)


    def resize_figure(self, width, height, dpi):
        self.figure.set_size_inches(width, height)
        self.figure.set_dpi(dpi)
        self.draw()


class Graphic(QWidget):
    limitInvalid = pyqtSignal()
    limitChanged = pyqtSignal()

    def __init__(
            self,
            text_primary_color: str,
            hover_color: str,
            second_background_color: str,
            parent: QWidget = None
    ):
        super().__init__(parent)

        self.fig_width = self.width() / self.physicalDpiX() * 1.5,
        self.fig_height = self.height() / self.physicalDpiY() * 1.5,

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        y_max = InputLabel(text_primary_color)
        y_max.setFixedWidth(30)
        y_max.setFixedHeight(30)
        self._y_max = y_max

        y_min = InputLabel(text_primary_color)
        y_min.setFixedWidth(30)
        y_min.setFixedHeight(30)
        self._y_min = y_min

        x_max = InputLabel(text_primary_color)
        x_max.setFixedWidth(30)
        x_max.setFixedHeight(30)
        self._x_max = x_max

        x_min = InputLabel(text_primary_color)
        x_min.setFixedWidth(30)
        x_min.setFixedHeight(30)
        self._x_min = x_min

        graphic = Canvas()
        graphic.setStyleSheet("""
            QWidget {
                border: 1px solid $HOVER;
                border-radius: 5px;
                background-color: $BG2;
            }
        """.replace(
            "$HOVER", hover_color,
        ).replace(
            "$BG2", second_background_color,
        ))
        graphic.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QColor(0, 0, 0, 50),
            offset=QPointF(0, 0)
        ))
        self._graphic = graphic

        toolbar = NavigationToolbar(graphic, self)
        self._toolbar = toolbar

        layout.addWidget(y_max, 0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(x_min, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(graphic, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(x_max, 1, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(y_min, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(toolbar, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        y_max.finishEditing.connect(self.limit_changed)
        y_min.finishEditing.connect(self.limit_changed)
        x_max.finishEditing.connect(self.limit_changed)
        x_min.finishEditing.connect(self.limit_changed)

    def y_limits(self) -> tuple[float, float]:
        return float(self._y_min.text()), float(self._y_max.text())

    def x_limits(self) -> tuple[float, float]:
        return float(self._x_min.text()), float(self._x_max.text())

    def limit_changed(self):
        y_max = self._y_max.text()
        y_min = self._y_min.text()
        x_max = self._x_max.text()
        x_min = self._x_min.text()

        if not y_max or not y_min or not x_max or not x_min:
            self.limitInvalid.emit()
            return

        try:
            float(y_max)
            float(y_min)
            float(x_max)
            float(x_min)
        except ValueError:
            self.limitInvalid.emit()
            return

        self.limitChanged.emit()

    def set_y_limits(self, y_limits: tuple[float, float]):
        self._graphic.ax.set_ylim(y_limits)
        self._y_max.setText(str(y_limits[1]))
        self._y_min.setText(str(y_limits[0]))

    def set_x_limits(self, x_limits: tuple[float, float]):
        self._graphic.ax.set_xlim(x_limits)
        self._x_max.setText(str(x_limits[1]))
        self._x_min.setText(str(x_limits[0]))

    def set_graphic(self, figure: Figure):
        if self._graphic.figure:
            self._graphic.figure.clear()
        self._graphic.figure = figure
        self._graphic.draw()
