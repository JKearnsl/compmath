from PyQt6 import QtCore, QtWidgets

from compmath.views.widgets import WidgetsFactory


class UISLATPage:
    def setup_ui(self, page: QtWidgets.QWidget, widgets_factory: WidgetsFactory):
        page.setObjectName("page")
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        scroll_area = QtWidgets.QScrollArea(page)
        scroll_area.setObjectName("scroll_area")
        scroll_area.setStyleSheet("""
            QWidget#scroll_area {
                background-color: $BG1;
                border: none;
                outline: none;
            }
        """.replace(
            "$BG1", widgets_factory.theme.first_background)
        )
        scroll_area.setWidgetResizable(True)
        page_layout.addWidget(scroll_area)

        central_layout = QtWidgets.QVBoxLayout(scroll_area)
        central_layout.setContentsMargins(30, 20, 30, 20)
        central_layout.setSpacing(10)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        # Body


        central_layout.addStretch(1)
        self.translate_ui(page)
        QtCore.QMetaObject.connectSlotsByName(page)

    def translate_ui(self, page: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
