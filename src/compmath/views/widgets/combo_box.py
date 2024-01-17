from PyQt6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(
            self,
            selection_color: str,
            primary_text_color: str,
            first_background_color: str,
            second_background_color: str,
            third_background_color: str,
            hover_color: str,
            parent=None
    ):
        super().__init__(parent)

        self.setStyleSheet("""
            QComboBox {
                border: 2px solid $SELECTION;
                border-radius: 5px;
                padding: 1px 10px 1px 3px;
                background: transparent;
                color: $PRIMARY_TEXT_COLOR;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: $SELECTION;
                border-left-style: solid;
                background: $SELECTION;
            }
            
            QComboBox::down-arrow {
                image: url(icons:drop-down-arrow.png);
                width: 9px;
                height: 9px;
            }
            
            QComboBox::disabled {
                background: $BG2;
                color: $BG1;
                font-weight: bold;
            }
            
            QComboBox::down-arrow:disabled{
                image: url(icons:drop-down-arrow-gray.png);
                width: 9px;
                height: 9px;
            }
            
            QComboBox QAbstractItemView {
                border: 1px solid $SELECTION;
                border-radius: 5px;
                background: $BG2;
                color: $PRIMARY_TEXT_COLOR;
                outline: none;
            }
            
            QComboBox::item {
                color: $PRIMARY_TEXT_COLOR;
                height: 25px;
                margin: 4px;
                spacing: 3px;
                padding: 1px 5px;
                border-radius: 4px;
                background: transparent;
                
            }
            
            QComboBox::item:selected {
                background-color: $HOVER_COLOR;
            }
            
            
        """.replace(
            "$SELECTION", selection_color,
        ).replace(
            "$PRIMARY_TEXT_COLOR", primary_text_color,
        ).replace(
            "$BG1", first_background_color,
        ).replace(
            "$BG2", second_background_color,
        ).replace(
            "$BG3", third_background_color,
        ).replace(
            "$HOVER_COLOR", hover_color,
        ))
