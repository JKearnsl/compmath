from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidget


class Table(QTableWidget):
    def __init__(
            self,
            selection_color,
            primary_text_color,
            hover_color,
            third_background_color,
            parent=None
    ):
        super().__init__(parent)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QTableWidget {
                border: 2px solid $HOVER;
                border-radius: 5px;
                background: $BG3;
                color: $PRIMARY_TEXT_COLOR;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background: $SELECTION;
                color: $PRIMARY_TEXT_COLOR;
            }
            QTableWidget::item:hover {
                background: $HOVER;
                color: $PRIMARY_TEXT_COLOR;
            }
            
            QHeaderView::section {
                background: $BG3;
                color: $PRIMARY_TEXT_COLOR;
                padding: 5px;
                border-bottom: 2px solid $HOVER;
            }
            QHeaderView::section:hover {
                background: $HOVER;
            }
            
            QScrollBar:vertical {
                border: none;
                background: $BG3;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: $HOVER;
                border-radius: 2px;
                min-height: 0px;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            
        """.replace(
            "$SELECTION", selection_color
        ).replace(
            "$PRIMARY_TEXT_COLOR", primary_text_color
        ).replace(
            "$HOVER", hover_color
        ).replace(
            "$BG3", third_background_color
        ))

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)
