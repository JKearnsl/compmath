from PyQt6.QtWidgets import QSpinBox


class SpinBox(QSpinBox):
    def __init__(
            self,
            selection_color: str,
            primary_text_color: str,
            first_background_color: str,
            second_background_color: str,
            parent=None
    ):
        super().__init__(parent)

        self.setStyleSheet("""
            QSpinBox {
                border: 2px solid $SELECTION;
                border-radius: 5px;
                padding: 1px 10px 1px 3px;
                background: transparent;
                color: $PRIMARY_TEXT_COLOR;
            }
            
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 15px;
                height: 12.5px;
                border-left-width: 1px;
                border-left-color: $SELECTION;
                border-left-style: solid;
                border-top-right-radius: 5px;
                background: $SELECTION;
            }
            
            QSpinBox::up-arrow {
                image: url(icons:drop-up-arrow.png);
                width: 9px;
                height: 9px;
            }
            
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 15px;
                height: 12.5px;
                border-left-width: 1px;
                border-left-color: $SELECTION;
                border-left-style: solid;
                border-bottom-right-radius: 5px;
                background: $SELECTION;
            }

            QSpinBox::down-arrow {
                image: url(icons:drop-down-arrow.png);
                width: 9px;
                height: 9px;
            }
            
            QSpinBox::disabled {
                background: $BG2;
                color: $BG1;
                font-weight: bold;
            }
            
            QSpinBox::up-arrow:disabled{
                image: url(icons:drop-up-arrow-gray.png);
                width: 9px;
                height: 9px;
            }
            
            QSpinBox::down-arrow:disabled{
                image: url(icons:drop-down-arrow-gray.png);
                width: 9px;
                height: 9px;
            }
            
            
        """.replace(
            "$SELECTION", selection_color,
        ).replace(
            "$PRIMARY_TEXT_COLOR", primary_text_color,
        ).replace(
            "$BG1", first_background_color,
        ).replace(
            "$BG2", second_background_color,
        ))
