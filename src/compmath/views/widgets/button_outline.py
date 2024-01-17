from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QPushButton


class ButtonOutline(QPushButton):
    def __init__(
            self,
            text_color,
            hover_color,
            parent=None
    ):
        super().__init__(parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid $TEXT_COLOR;
                border-radius: 4px;
                font-weight: bold;
                padding: 4px;
                color: $TEXT_COLOR
            }
            QPushButton:hover {
                border: 2px solid $TEXT_HOVER;
                color: $TEXT_HOVER;
            }
            QPushButton:pressed {
                color: $TEXT_COLOR;
            }
            
            QPushButton:disabled {
                color: $TEXT_HOVER;
            }
        """.replace(
            "$TEXT_COLOR", text_color
        ).replace(
            "$TEXT_HOVER", hover_color
        ))
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)