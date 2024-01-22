from PyQt6 import QtCore, QtWidgets

from compmath.views.widgets import WidgetsFactory


class UiNIPage:
    def setup_ui(self, page: QtWidgets.QWidget, widgets_factory: WidgetsFactory):
        page.setObjectName("page")
        page_layout = QtWidgets.QHBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        sheet = QtWidgets.QWidget(page)
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
                    QWidget#sheet {
                        background-color: $BG1;
                    }
                """.replace(
            "$BG1", widgets_factory.theme.first_background
        ))
        page_layout.addWidget(sheet)

        central_layout = QtWidgets.QVBoxLayout(sheet)
        central_layout.setContentsMargins(30, 20, 30, 20)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        central_layout.setSpacing(10)
        self.central_layout = central_layout
        sheet.setLayout(central_layout)

        scroll_area = QtWidgets.QScrollArea(page)
        scroll_area.setObjectName("scroll_area")
        scroll_area.setStyleSheet("""
                    QWidget#scroll_area {
                        border: none;
                        outline: none;
                    }
                """)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(sheet)
        page_layout.addWidget(scroll_area)

        # Body


        central_layout.addStretch(1)
        self.translate_ui(page)
        QtCore.QMetaObject.connectSlotsByName(page)

    def translate_ui(self, page: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
