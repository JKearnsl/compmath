from PyQt6.QtWidgets import QLabel


class Label(QLabel):
    def __init__(self, color, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: $PRIMARY_TEXT_COLOR;
            }
        
        """.replace(
            "$PRIMARY_TEXT_COLOR", color,
        ))

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)
