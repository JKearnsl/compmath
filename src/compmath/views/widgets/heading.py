from PyQt6.QtWidgets import QLabel


class Heading1(QLabel):
    def __init__(self, color, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                color: $HEADER_TEXT_COLOR;
                font-size: 32px;
                font-weight: bold;
            }

        """.replace(
            "$HEADER_TEXT_COLOR", color,
        ))
        self.setFixedHeight(50)


class Heading2(QLabel):
    def __init__(self, color, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                color: $HEADER_TEXT_COLOR;
                font-size: 24px;
                font-weight: bold;
            }

        """.replace(
            "$HEADER_TEXT_COLOR", color,
        ))
        self.setFixedHeight(50)


class Heading3(QLabel):
    def __init__(self, color, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                color: $HEADER_TEXT_COLOR;
                font-size: 18px;
                font-weight: bold;
            }

        """.replace(
            "$HEADER_TEXT_COLOR", color,
        ))
        self.setFixedHeight(50)


class Heading4(QLabel):
    def __init__(self, color, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                color: $HEADER_TEXT_COLOR;
                font-size: 16px;
                font-weight: bold;
            }

        """.replace(
            "$HEADER_TEXT_COLOR", color,
        ))
        self.setFixedHeight(50)


class Heading5(QLabel):
    def __init__(self, color, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                color: $HEADER_TEXT_COLOR;
                font-size: 13px;
                font-weight: bold;
            }

        """.replace(
            "$HEADER_TEXT_COLOR", color,
        ))
        self.setFixedHeight(50)


class Heading6(QLabel):
    def __init__(self, color, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                color: $HEADER_TEXT_COLOR;
                font-size: 10px;
                font-weight: bold;
            }

        """.replace(
            "$HEADER_TEXT_COLOR", color,
        ))
        self.setFixedHeight(50)
