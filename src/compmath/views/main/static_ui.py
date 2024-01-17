from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QStackedLayout,
    QWidget,
    QHBoxLayout,
    QMenu,
    QToolButton,
    QLabel
)

from compmath.models.main import MenuItem
from compmath.utils.icon import svg_ico
from compmath.views.widgets import WidgetsFactory, Label
from compmath.views.widgets.list import ListItemWidget


class UiMainWindow:
    def setup_ui(
            self,
            main_window: QWidget,
            widgets_factory: WidgetsFactory,
            version: str,
            app_name: str,
    ):
        main_window.setObjectName("main_window")
        main_window.setWindowTitle(app_name)
        main_window.resize(900, 600)
        main_window.setStyleSheet("""
            QWidget#main_window {
                background-color: $BG1;
            }
            QToolTip {
                background: #D9DBDD;
                border: 1px solid #000000;
                border-radius: 3px;
                color: #000000;
            }
        """.replace("$BG1", widgets_factory.theme.first_background))
        central_layout = QHBoxLayout(main_window)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Menu widget
        menu_widget = QWidget(main_window)
        menu_widget.setObjectName("menu_widget")
        menu_widget.setStyleSheet("""
            QWidget#menu_widget {
                background-color: $BG2;
                border-right: 1px solid $HOVER;
            }
        """.replace(
            "$BG2", widgets_factory.theme.second_background
        ).replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        menu_widget.setFixedWidth(270)
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(menu_widget)

        # Menu header
        menu_header_widget = QWidget()
        menu_header_widget.setObjectName("menu_header_widget")
        menu_header_widget.setToolTip(f"{app_name} {version}")
        menu_layout.addWidget(menu_header_widget)

        menu_header_layout = QHBoxLayout(menu_header_widget)
        menu_header_layout.setContentsMargins(20, 15, 20, 10)

        # Menu header info widget
        info_stub = QWidget()
        info_stub.setObjectName("menu_header_logo_widget")
        info_stub.setFixedHeight(50)

        menu_header_info_layout = QHBoxLayout(info_stub)
        menu_header_info_layout.setContentsMargins(0, 0, 0, 0)
        menu_header_info_layout.setSpacing(5)
        menu_header_layout.addWidget(info_stub)

        logo = QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(main_window.windowIcon().pixmap(QtCore.QSize(64, 64)))
        logo.setScaledContents(True)
        logo.setFixedSize(QtCore.QSize(32, 32))
        menu_header_info_layout.addWidget(logo)

        program_title_layout = QVBoxLayout()
        program_title_layout.setContentsMargins(4, 3, 0, 3)
        program_title_layout.setSpacing(0)
        menu_header_info_layout.addLayout(program_title_layout)

        title_widget = QLabel()
        self.title_widget = title_widget
        title_widget.setObjectName("title_widget")
        title_widget.setText(app_name)
        title_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        title_widget.setStyleSheet("""
            QLabel#title_widget {
                font-size: 14px;
                font-weight: 800;
                color: $TEXT_HEADER;
            }
        """.replace(
            "$TEXT_HEADER", widgets_factory.theme.text_header
        ))
        program_title_layout.addWidget(title_widget)

        description_widget = QLabel()
        self.description_widget = description_widget
        description_widget.setObjectName("description_widget")
        description_widget.setText(version)
        description_widget.setStyleSheet("""
            QLabel#description_widget {
                font-size: 12px;
                font-weight: bold;
                color: $TEXT_SECONDARY;
            }
        """.replace(
            "$TEXT_SECONDARY", widgets_factory.theme.text_secondary
        ))
        program_title_layout.addWidget(description_widget)

        menu_header_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        )

        # Menu list
        menu_list_widget = widgets_factory.list()
        menu_list_widget.setObjectName("menu_list_widget")
        menu_list_widget.setIconSize(QtCore.QSize(16, 16))
        menu_list_model = menu_list_widget.model()
        self.menu_select_model = menu_list_widget.selectionModel()

        self.menu_item_research = ListItemWidget("Menu item 1", MenuItem.RESEARCH, "icons:research.svg")
        self.menu_item_nonlinear = ListItemWidget("Menu item 2", MenuItem.NONLINEAR, "icons:nonlinear.svg")
        self.menu_item_slat = ListItemWidget("Menu item 3", MenuItem.SLAT, "icons:slat.svg")
        self.menu_item_ni = ListItemWidget("Menu item 4", MenuItem.NI, "icons:ni.svg")
        self.menu_item_sne = ListItemWidget("Menu item 5", MenuItem.SNE, "icons:sne.svg")
        self.menu_item_aif = ListItemWidget("Menu item 6", MenuItem.AIF, "icons:aif.svg")

        menu_list_model.appendRow(self.menu_item_research)
        menu_list_model.appendRow(self.menu_item_nonlinear)
        menu_list_model.appendRow(self.menu_item_slat)
        menu_list_model.appendRow(self.menu_item_ni)
        menu_list_model.appendRow(self.menu_item_sne)
        menu_list_model.appendRow(self.menu_item_aif)

        menu_layout.addWidget(menu_list_widget)
        self.menu_list_widget = menu_list_widget

        # Tool section
        menu_tool_layout = QHBoxLayout()
        menu_settings_button = QToolButton()
        menu_settings_button.setObjectName("menu_settings_button")
        menu_settings_button.setIcon(svg_ico("icons:settings.svg", widgets_factory.theme.text_secondary))
        menu_settings_button.setIconSize(QtCore.QSize(20, 20))
        menu_settings_button.setStyleSheet("""
            QToolButton#menu_settings_button {
                border-radius: 10px;
                background-color: transparent;
            }
            QToolButton#menu_settings_button:hover {
                background-color: $HOVER;
            }
            QToolButton#menu_settings_button:pressed {
                background-color: transparent;
            }
        """.replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        self.menu_settings_button = menu_settings_button

        memory_usage_label = Label(widgets_factory.theme.text_secondary)
        memory_usage_label.setObjectName("memory_usage_label")
        memory_usage_label.add_style("""
            QLabel#memory_usage_label {
                font-size: 12px;
                font-weight: bold;
                }
        """)
        self.memory_usage_label = memory_usage_label

        # Context menu
        context_menu = QMenu(main_window)
        context_menu.setObjectName("context_menu")
        context_menu.setStyleSheet("""
            QMenuBar {
                background-color: transparent;
            }

            QMenuBar::item {
                color : $TEXT_PRIMARY_COLOR;
                margin-top:4px;
                spacing: 3px;
                padding: 1px 10px;
                background: transparent;
                border-radius: 4px;
            }


            QMenuBar::item:selected {
                background: $BG2;
            }

            QMenuBar::item:pressed {
                background: $SELECTED_COLOR;
                color: #FFFFFF;
            }

            QMenu {
                background-color: $BG1;
                border: 1px solid $HOVER_COLOR;
                border-top-right-radius: 5px;
                border-top-left-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QMenu::item {
                color: $TEXT_PRIMARY_COLOR;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: $HOVER_COLOR;
            } 
                """.replace(
            "$TEXT_PRIMARY_COLOR", widgets_factory.theme.text_primary
        ).replace(
            "$BG2", widgets_factory.theme.second_background
        ).replace(
            "$SELECTED_COLOR", widgets_factory.theme.primary
        ).replace(
            "$BG1", widgets_factory.theme.first_background
        ).replace(
            "$HOVER_COLOR", widgets_factory.theme.hover
        ))
        self.settings_item = context_menu.addAction("Settings")
        self.about_item = context_menu.addAction("About")
        self.context_menu = context_menu

        menu_tool_layout.addItem(
            QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        )
        menu_tool_layout.addWidget(menu_settings_button)
        menu_tool_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        menu_tool_layout.addWidget(memory_usage_label)
        menu_tool_layout.addItem(
            QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        )
        menu_layout.addLayout(menu_tool_layout)
        menu_layout.addItem(
            QSpacerItem(0, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        )

        # Content layout
        content_layout = QStackedLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.setObjectName("content_widget")
        central_layout.addLayout(content_layout)
        self.content_layout = content_layout

        self.translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        self.menu_item_research.setText(_translate("main_window", "Методы исследования"))
        self.menu_item_nonlinear.setText(_translate("main_window", "Нелинейные уравнения"))
        self.menu_item_slat.setText(_translate("main_window", "СЛАУ"))
        self.menu_item_ni.setText(_translate("main_window", "Численные интегрирования"))
        self.menu_item_sne.setText(_translate("main_window", "Системы нелинейных уравнений"))
        self.menu_item_aif.setText(_translate("main_window", "Аппроксимация и интерполяция"))

        self.settings_item.setText(_translate("settings_item", "Настройки"))
        self.about_item.setText(_translate("about_item", "О программе"))
