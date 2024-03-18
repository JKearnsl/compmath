import logging

from PyQt6 import sip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QVector3D
from PyQt6.QtWidgets import (
    QWidget,
    QToolButton,
    QVBoxLayout
)
from pyqtgraph.opengl import GLViewWidget, GLGraphicsItem, GLAxisItem
from OpenGL import error as opengl_error
from compmath.utils.icon import svg_ico
from compmath.views.widgets import Dialog


class GLCanvas(GLViewWidget):
    def __init__(self, background_color: str = "white", parent=None):
        super().__init__(parent)

        self.opts['distance'] = 10
        self.setBackgroundColor(background_color)

        self.axis = GLAxisItem(
            size=QVector3D(100, 100, 100),
        )
        self.addItem(self.axis)

    def addItem(self, item: GLGraphicsItem):
        if self and not sip.isdeleted(self):
            super().addItem(item)
        else:
            logging.warning("[GLCanvas] self is deleted")

    def clearItems(self):
        if self and not sip.isdeleted(self):
            self.clear()
            self.addItem(self.axis)
        else:
            logging.warning("[GLCanvas] self is deleted")

    def paintGL(self, region=None, viewport=None, useItemNames=False):
        try:
            super().paintGL(region, viewport, useItemNames)
        except opengl_error.Error as error:
            logging.error(f"[GLCanvas] OpenGL Error in paintGL: {error}")


def copy_item(item: GLGraphicsItem) -> GLGraphicsItem:
    if isinstance(item, GLAxisItem):
        return GLAxisItem(size=item.size())
    return item


class GLWidget(QWidget):

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

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(0)
        sheet.setLayout(layout)

        gl_widget = GLCanvas(dialog_background_color, self)
        self._gl_widget = gl_widget

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
        fullscreen_btn.clicked.connect(self.show_full_screen)
        toolbar_layout.addWidget(fullscreen_btn)
        self.toolbar = toolbar

        layout.addWidget(gl_widget)
        layout.addWidget(toolbar)

    def set_element(self, element_items: list[GLGraphicsItem]):
        self._gl_widget.clearItems()
        for item in element_items:
            self._gl_widget.addItem(item)

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

        # graphic = GLCanvas(self._dialog_background_color, self)
        # for item in self._gl_widget.items:
        #     graphic.addItem(copy_item(item))
        # dialog.layout().addWidget(graphic)

        dialog.show()

    def setFixedHeight(self, a0: int) -> None:
        self._gl_widget.setFixedHeight(a0 - 50)
        super().setFixedHeight(a0)

    def setFixedWidth(self, a0: int) -> None:
        self._gl_widget.setFixedWidth(a0)
        super().setFixedWidth(a0)
