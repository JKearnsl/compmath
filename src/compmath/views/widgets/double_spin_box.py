from PyQt6.QtCore import QLocale
from PyQt6.QtWidgets import QDoubleSpinBox


class DoubleSpinBox(QDoubleSpinBox):
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
            DoubleSpinBox {
                border: 2px solid $SELECTION;
                border-radius: 5px;
                padding: 1px 10px 1px 3px;
                background: transparent;
                color: $PRIMARY_TEXT_COLOR;
            }

            DoubleSpinBox::up-button {
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

            DoubleSpinBox::up-arrow {
                image: url(icons:drop-up-arrow.png);
                width: 9px;
                height: 9px;
            }

            DoubleSpinBox::down-button {
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

            DoubleSpinBox::down-arrow {
                image: url(icons:drop-down-arrow.png);
                width: 9px;
                height: 9px;
            }

            DoubleSpinBox::disabled {
                background: $BG2;
                color: $BG1;
                font-weight: bold;
            }

            DoubleSpinBox::up-arrow:disabled{
                image: url(icons:drop-up-arrow-gray.png);
                width: 9px;
                height: 9px;
            }

            DoubleSpinBox::down-arrow:disabled{
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

    def textFromValue(self, value: float) -> str:
        return QLocale().toString(value, 'g', QLocale.FloatingPointPrecisionOption.FloatingPointShortest)
