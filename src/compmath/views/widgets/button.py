from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect


class Button(QPushButton):
    def __init__(
            self,
            hover_color,
            background_color,
            text_hover_color,
            text_color,
            text_color_disabled,
            parent=None
    ):
        super().__init__(parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: $BG;
                border: 1px solid #00000000;
                border-radius: 4px;
                padding: 2px 4px;
                color: $TEXT_COLOR;
            }
            QPushButton:hover {
                background-color: $HOVER;
                color: $TEXT_HOVER;
            }
            QPushButton:pressed {
                background-color: $BG;
                color: $TEXT_COLOR;
            }
            
            QPushButton:disabled {
                background-color: $HOVER;
                color: $TEXT_DISABLED;
            }
        """.replace(
            "$HOVER", hover_color,
        ).replace(
            "$TEXT_COLOR", text_color
        ).replace(
            "$BG", background_color
        ).replace(
            "$TEXT_HOVER", text_hover_color
        ).replace(
            "$TEXT_DISABLED", text_color_disabled
        ))

        self.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor(0, 0, 0, 50),
            offset=QtCore.QPointF(0, 0)
        ))
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)
