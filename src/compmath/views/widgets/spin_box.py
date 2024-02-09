from PyQt6.QtWidgets import QSpinBox


class SpinBox(QSpinBox):
    def __init__(
            self,
            selection_color: str,
            text_color: str,
            background_color: str,
            disabled_text_color: str,
            hover_color: str,
            parent=None
    ):
        super().__init__(parent)

        self.setStyleSheet("""
            QSpinBox {
                border: 2px solid $HOVER;
                border-radius: 5px;
                padding: 1px 10px 1px 3px;
                background: $BG;
                color: $TEXT_COLOR;
            }
            
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 15px;
                height: 12.5px;
                border-left-width: 1px;
                border-left-color: $HOVER;
                border-left-style: solid;
                border-top-right-radius: 5px;
                background: $HOVER;
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
                border-left-color: $HOVER;
                border-left-style: solid;
                border-bottom-right-radius: 5px;
                background: $HOVER;
            }
            
            QSpinBox::focus {
                border: 2px solid $SELECTION;
            }
            
            QSpinBox::up-button:focus {
                background: $SELECTION;
            } 
            
            QSpinBox::down-button:focus {
                background: $SELECTION;
            } 

            QSpinBox::down-arrow {
                image: url(icons:drop-down-arrow.png);
                width: 9px;
                height: 9px;
            }
            
            QSpinBox::disabled {
                background: $BG;
                color: $DISABLED_TEXT;
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
            "$TEXT_COLOR", text_color,
        ).replace(
            "$DISABLED_TEXT", disabled_text_color,
        ).replace(
            "$BG", background_color,
        ).replace(
            "$HOVER", hover_color
        ))
