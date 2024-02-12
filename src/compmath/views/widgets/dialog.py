from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLayout,
    QHBoxLayout,
    QWidget,
    QGraphicsDropShadowEffect,
    QLabel
)


class Dialog(QDialog):

    def __init__(
            self,
            background_window,
            background_close_btn,
            hover_close_btn,
            text_color_close_btn,
            parent=None
    ):
        super().__init__(parent)
        self.setModal(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(400, 300)

        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.setSpacing(0)

        shadow_sheet = QWidget(self)
        shadow_sheet.setObjectName("shadow_sheet")
        shadow_sheet.setStyleSheet(
            """
                QWidget#shadow_sheet {
                    border-radius: 10px;
                }
            """
        )
        dialog_layout.addWidget(shadow_sheet)

        shadow_sheet_layout = QHBoxLayout(shadow_sheet)
        shadow_sheet_layout.setContentsMargins(5, 5, 5, 5)
        shadow_sheet_layout.setSpacing(0)

        sheet = QWidget(shadow_sheet)
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
            QWidget#sheet {
                background-color: $BG;
                border-radius: 10px;
            }
        """.replace(
            "$BG", background_window
        ))
        sheet.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor(0, 0, 0, 50),
            offset=QtCore.QPointF(0, 0)
        ))
        shadow_sheet_layout.addWidget(sheet)

        general_layout = QVBoxLayout(sheet)
        general_layout.setContentsMargins(0, 0, 0, 0)
        general_layout.setSpacing(5)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        general_layout.addLayout(header_layout)

        # Close button
        exit_button = QPushButton(self)
        exit_button.setFixedSize(30, 30)
        exit_button.setText("×")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: $BG2;
                border-bottom-left-radius: 10px;
                border-top-right-radius: 10px;
                color: $TEXT_HEADER;
                font-size: 26px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: $HOVER;
            }
            QPushButton:pressed {
                background-color: $BG2;
            }
        """.replace(
            "$BG2", background_close_btn
        ).replace(
            "$HOVER", hover_close_btn
        ).replace(
            "$TEXT_HEADER", text_color_close_btn
        ))

        exit_button.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor(0, 0, 0, 50),
            offset=QtCore.QPointF(-1, 0)
        ))
        exit_button.clicked.connect(self.close)

        # Title
        title_widget = QWidget(self)
        title_widget.hide()
        title_widget.setFixedSize(
            self.width() - exit_button.width() - (30 * self.width() // 100),
            30
        )
        title_widget.setStyleSheet("""
            QWidget {
                background-color: $BG2;
            
                border-top-left-radius: 10px;
                border-bottom-right-radius: 10px;
                color: $TEXT_HEADER;
                font-size: 26px;
                font-weight: bold;
            }
        """.replace(
            "$BG2", background_close_btn
        ).replace(
            "$TEXT_HEADER", text_color_close_btn
        ))

        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(10, 0, 0, 0)
        title_layout.setSpacing(0)

        title_label = QLabel(self)
        title_label.setObjectName("title_label")
        title_label.setStyleSheet("""
            QLabel#title_label {
                color: $TEXT_HEADER;
                font-size: 12px;
                font-weight: bold;
            }
        """.replace(
            "$TEXT_HEADER", text_color_close_btn
        ))
        self._title_label = title_label
        title_layout.addWidget(title_label)
        self._title_widget = title_widget
        title_widget.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor(0, 0, 0, 50),
            offset=QtCore.QPointF(0, 0)
        ))

        header_layout.addWidget(title_widget)
        header_layout.addStretch(1)
        header_layout.addWidget(exit_button)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        general_layout.addLayout(self._layout)
        general_layout.addStretch(1)

    def layout(self) -> QLayout | None:
        return self._layout

    def setWindowTitle(self, title: str):
        super().setWindowTitle(title)
        if title:
            self._title_label.setText(title)
            self._title_widget.show()
        else:
            self._title_widget.hide()
