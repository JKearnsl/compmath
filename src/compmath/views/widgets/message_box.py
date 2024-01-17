from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QVBoxLayout, QLayout, QHBoxLayout, QWidget, QLabel

from compmath.views.widgets import Dialog


class MessageBox(Dialog):

    def __init__(
            self,
            title: str,
            content: str,
            icon: QtGui.QIcon,
            background_window,
            background_close_btn,
            hover_close_btn,
            text_color_close_btn,
            parent=None
    ):
        super().__init__(
            background_window,
            background_close_btn,
            hover_close_btn,
            text_color_close_btn,
            parent
        )
        self.setFixedSize(320, 350)

        self.setObjectName(f"message_box_{title.replace(' ', '_')}")

        content_layout = self.layout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        customize_sheet = QWidget(self)
        customize_sheet.setObjectName("customize_sheet")
        content_layout.addWidget(customize_sheet)

        central_layout = QHBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(20)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        # Logo
        icon_layout = QVBoxLayout()
        icon_layout.setContentsMargins(0, 5, 0, 0)
        icon_layout.setSpacing(10)

        icon_widget = QLabel()
        icon_widget.setObjectName("icon")
        icon_widget.setPixmap(icon.pixmap(QtCore.QSize(32, 32)))
        icon_widget.setScaledContents(True)
        icon_widget.setFixedSize(QtCore.QSize(32, 32))
        icon_layout.addWidget(icon_widget)

        icon_layout.addStretch(1)
        central_layout.addLayout(icon_layout)

        # Text
        text_widget = QLabel(parent=self)
        text_widget.setObjectName("text_widget")
        text_widget.setTextFormat(QtCore.Qt.TextFormat.MarkdownText)
        text_widget.setOpenExternalLinks(True)
        text_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        text_widget.setWordWrap(True)
        text_widget.setText(
            f"### {title}\n\n"
            f"{content}\n\n\n"
        )
        central_layout.addWidget(text_widget)

    def layout(self) -> QLayout | None:
        return self._layout
