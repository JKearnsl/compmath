from PyQt6 import QtCore, QtWidgets

from compmath.views.widgets import WidgetsFactory


class UiSettings:
    def setup_ui(self, settings_page: QtWidgets.QWidget, widgets_factory: WidgetsFactory):
        settings_page.setObjectName("settings_page")

        settings_page_layout = settings_page.layout()
        settings_page_layout.setContentsMargins(0, 0, 0, 0)
        settings_page_layout.setSpacing(0)

        customize_sheet = QtWidgets.QWidget(settings_page)
        customize_sheet.setObjectName("customize_sheet")
        settings_page_layout.addWidget(customize_sheet)

        central_layout = QtWidgets.QVBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(10)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)

        # Change Theme
        ch_theme_layout = QtWidgets.QVBoxLayout()
        ch_theme_layout.setContentsMargins(0, 0, 0, 0)
        ch_theme_layout.setSpacing(10)

        ch_theme_header = widgets_factory.heading3(parent=settings_page)
        ch_theme_header.setObjectName("ch_theme_header")
        ch_theme_layout.addWidget(ch_theme_header)
        self.ch_theme_header = ch_theme_header

        ch_color_theme_widget = widgets_factory.combo_box(parent=settings_page)
        ch_color_theme_widget.setObjectName("ch_color_theme_widget")
        ch_theme_layout.addWidget(ch_color_theme_widget)
        self.ch_color_theme_widget = ch_color_theme_widget

        central_layout.addLayout(ch_theme_layout)

        # Change Font
        ch_font_layout = QtWidgets.QVBoxLayout()
        ch_font_layout.setContentsMargins(0, 0, 0, 0)
        ch_font_layout.setSpacing(10)

        ch_font_header = widgets_factory.heading3(parent=settings_page)
        ch_font_header.setObjectName("ch_font_header")
        ch_font_layout.addWidget(ch_font_header)
        self.ch_font_header = ch_font_header

        ch_font_size_layout = QtWidgets.QHBoxLayout()
        ch_font_size_layout.setContentsMargins(0, 0, 0, 0)
        ch_font_size_layout.setSpacing(10)

        ch_font_size_label = widgets_factory.label(parent=settings_page)
        ch_font_size_label.setObjectName("ch_font_size_label")
        ch_font_size_layout.addWidget(ch_font_size_label)
        self.ch_font_size_label = ch_font_size_label

        ch_font_size_widget = widgets_factory.spin_box(parent=settings_page)
        ch_font_size_widget.setObjectName("ch_font_size_widget")
        ch_font_size_widget.setMinimum(0)
        ch_font_size_widget.setMaximum(100)
        ch_font_size_widget.setValue(settings_page.font().pointSize())
        ch_font_size_widget.setDisabled(True)
        ch_font_size_layout.addWidget(ch_font_size_widget)

        ch_font_layout.addLayout(ch_font_size_layout)
        central_layout.addLayout(ch_font_layout)

        # Change theme dialog
        ch_color_theme_dialog = widgets_factory.modal(parent=settings_page)
        ch_color_theme_dialog.setObjectName("ch_color_theme_dialog")
        ch_color_theme_dialog.setFixedSize(400, 250)

        ch_color_theme_dialog_layout = ch_color_theme_dialog.layout()
        ch_color_theme_dialog_layout.setContentsMargins(15, 10, 15, 10)
        ch_color_theme_dialog_layout.setSpacing(10)

        ch_color_theme_dialog_header = widgets_factory.heading3(parent=settings_page)
        ch_color_theme_dialog_header.setObjectName("ch_color_theme_dialog_header")
        ch_color_theme_dialog_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        ch_color_theme_dialog_layout.addWidget(ch_color_theme_dialog_header)
        self.ch_color_theme_dialog_header = ch_color_theme_dialog_header

        ch_color_theme_dialog_text = widgets_factory.label(parent=settings_page)
        ch_color_theme_dialog_text.setObjectName("ch_color_theme_dialog_text")
        ch_color_theme_dialog_text.setWordWrap(True)
        ch_color_theme_dialog_layout.addWidget(ch_color_theme_dialog_text)
        self.ch_color_theme_dialog_text = ch_color_theme_dialog_text

        ch_color_theme_dialog_buttons_layout = QtWidgets.QHBoxLayout()
        ch_color_theme_dialog_buttons_layout.setContentsMargins(10, 10, 10, 10)
        ch_color_theme_dialog_buttons_layout.setSpacing(30)

        ch_color_theme_dialog_cancel_button = widgets_factory.button(parent=settings_page)
        ch_color_theme_dialog_cancel_button.setObjectName("ch_color_theme_dialog_cancel_button")
        ch_color_theme_dialog_cancel_button.clicked.connect(ch_color_theme_dialog.reject)
        ch_color_theme_dialog_buttons_layout.addWidget(ch_color_theme_dialog_cancel_button)
        self.ch_color_theme_dialog_cancel_button = ch_color_theme_dialog_cancel_button

        ch_color_theme_dialog_ok_button = widgets_factory.button(parent=settings_page)
        ch_color_theme_dialog_ok_button.setObjectName("ch_color_theme_dialog_ok_button")
        ch_color_theme_dialog_ok_button.clicked.connect(ch_color_theme_dialog.accept)
        ch_color_theme_dialog_buttons_layout.addWidget(ch_color_theme_dialog_ok_button)
        self.ch_color_theme_dialog_ok_button = ch_color_theme_dialog_ok_button

        ch_color_theme_dialog_layout.addLayout(ch_color_theme_dialog_buttons_layout)

        self.ch_color_theme_dialog = ch_color_theme_dialog

        self.translate_ui(settings_page)
        QtCore.QMetaObject.connectSlotsByName(settings_page)

    def translate_ui(self, settings_page: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        self.ch_theme_header.setText(
            _translate("settings_page_ch_theme_header", "Сменить тему")
        )
        self.ch_font_header.setText(
            _translate("settings_page_ch_font_header", "Сменить шрифт")
        )
        self.ch_font_size_label.setText(
            _translate("settings_page_ch_font_size_label", "Размер: ")
        )
        self.ch_color_theme_dialog.setWindowTitle(
            _translate("settings_page_ch_color_theme_dialog", "Смена оформления")
        )
        self.ch_color_theme_dialog_header.setText(
            _translate("settings_page_ch_color_theme_dialog_header", "Вы уверены что хотите сменить тему?")
        )
        self.ch_color_theme_dialog_text.setText(
            _translate(
                "settings_page_ch_color_theme_dialog_text",
                "Для смены цветовой темы необходимо перезапустить приложение. "
                "При перезапуске, все несохраненные данные будут утеряны."
            )
        )
        self.ch_color_theme_dialog_cancel_button.setText(
            _translate("cancel_button", "Отмена")
        )
        self.ch_color_theme_dialog_ok_button.setText(
            _translate("reboot_button", "Перезапуск")
        )


