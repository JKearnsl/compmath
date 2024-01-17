from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QLabel, QWidget, QStackedLayout, QLineEdit


class InputLabel(QWidget):
    startEditing = pyqtSignal()
    finishEditing = pyqtSignal()

    def __init__(self, color, parent=None):
        super().__init__(parent)

        layout = QStackedLayout()
        self.setLayout(layout)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: $TEXT_COLOR;
            }
        """.replace(
            "$TEXT_COLOR", color,
        ))
        layout.addWidget(self.label)

        self._input = QLineEdit()
        self._input.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: $TEXT_COLOR;
                border: 1px solid $TEXT_COLOR;
                border-radius: 3px;
                padding: 3px;
            }
        """.replace(
            "$TEXT_COLOR", color,
        ))
        layout.addWidget(self._input)
        layout.setCurrentWidget(self.label)

        self.mouseDoubleClickEvent = self.start_editing
        self._input.focusOutEvent = self.finish_editing

    def setText(self, text: str):
        self.label.setText(text)

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)

    def text(self):
        return self.label.text()

    def start_editing(self, event):
        self._input.setText(self.label.text())
        self._input.setFocus()
        self._input.selectAll()
        self.layout().setCurrentWidget(self._input)
        self.startEditing.emit()

    def finish_editing(self, event):
        self.label.setText(self._input.text())
        self.layout().setCurrentWidget(self.label)
        self.finishEditing.emit()
