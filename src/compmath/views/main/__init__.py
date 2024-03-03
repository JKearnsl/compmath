from PyQt6 import QtWidgets, QtCore, sip
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QWidget
from apscheduler.schedulers.qt import QtScheduler

from compmath.models.main import MainModel
from compmath.utils.observer import DObserver
from compmath.utils.ts_meta import TSMeta
from compmath.views.main.static_ui import UiMainWindow
from compmath.views.widgets import WidgetsFactory


class MainView(QWidget, DObserver, metaclass=TSMeta):

    def __init__(
            self,
            controller,
            model: MainModel,
            widgets_factory: WidgetsFactory,
            parent=None
    ):
        super().__init__(parent)
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        self.ui = UiMainWindow()
        self.ui.setup_ui(
            self,
            widgets_factory=widgets_factory,
            version=self.model.app_version,
            app_name=self.model.app_title
        )

        self.scheduler = QtScheduler()

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.menu_select_model.currentChanged.connect(self.menu_select_changed)
        self.ui.menu_settings_button.clicked.connect(self.menu_settings_button_clicked)
        self.ui.settings_item.triggered.connect(self.controller.show_settings)
        self.ui.about_item.triggered.connect(self.about_dialog)

    def model_changed(self):
        pass

    def process_stats_tick(self):
        info = self.model.process_info()
        ram_mb = info[0]
        ram_total_mb = info[1]
        ram_percent = info[2]
        cpu_percent = info[3]

        if self and not sip.isdeleted(self):
            self.ui.memory_usage_label.setText(f"ОЗУ: {ram_mb} МБ")
            self.ui.memory_usage_label.setToolTip(
                f"RAM {ram_percent:.2f}% [{ram_mb}/{ram_total_mb}] МБ\n"
                f"CPU {cpu_percent:.2f}%"
            )

    def model_loaded(self):
        for i in range(self.ui.menu_list_widget.model().rowCount()):
            item = self.ui.menu_list_widget.model().item(i)
            item.set_icon_color(self.widgets_factory.theme.text_tertiary)
        self.ui.menu_list_widget.setCurrentIndex(self.ui.menu_list_widget.model().index(0, 0))
        if self.model.is_debug:
            self.scheduler.add_job(self.process_stats_tick, 'interval', seconds=2)
            self.scheduler.start()

    def menu_select_changed(self, current: QModelIndex, prev: QModelIndex):
        item = self.ui.menu_list_widget.model().item(current.row())
        item.set_icon_color(self.widgets_factory.theme.text_primary)

        if self.ui.content_layout.count() > 0:
            current_widget = self.ui.content_layout.currentWidget()
            if current_widget.id == item.id:
                return

            prev_item = self.ui.menu_list_widget.model().item(prev.row())
            prev_item.set_icon_color(self.widgets_factory.theme.text_tertiary)

            # Кэш
            for i in range(self.ui.content_layout.count()):
                widget = self.ui.content_layout.widget(i)
                if widget.id == item.id:
                    self.ui.content_layout.setCurrentWidget(widget)
                    return

        self.controller.show_page(item.id)

    def about_dialog(self):
        modal = self.widgets_factory.modal(self)
        modal.setWindowTitle("О программе")
        modal.setFixedSize(320, 350)

        modal.setObjectName("modal")

        modal_layout = modal.layout()
        modal_layout.setContentsMargins(0, 0, 0, 0)
        modal_layout.setSpacing(0)

        customize_sheet = QtWidgets.QWidget(modal)
        customize_sheet.setObjectName("customize_sheet")
        modal_layout.addWidget(customize_sheet)

        central_layout = QtWidgets.QHBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(20)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        # Logo
        logo_layout = QtWidgets.QVBoxLayout()
        logo_layout.setContentsMargins(0, 5, 0, 0)
        logo_layout.setSpacing(10)

        logo = QtWidgets.QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(self.windowIcon().pixmap(QtCore.QSize(64, 64)))
        logo.setScaledContents(True)
        logo.setFixedSize(QtCore.QSize(32, 32))
        logo_layout.addWidget(logo)

        logo_layout.addStretch(1)
        central_layout.addLayout(logo_layout)

        # Text
        text_widget = self.widgets_factory.label(parent=modal)
        text_widget.setObjectName("text_widget")
        text_widget.setTextFormat(QtCore.Qt.TextFormat.MarkdownText)
        text_widget.setOpenExternalLinks(True)
        text_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        text_widget.setWordWrap(True)
        text_widget.setText(
            f"### {self.model.app_title} | {self.model.app_version}\n\n"
            "Программа разработана в рамках лабораторной работы\n\n\n"
            "Разработчик: "
            f"<a href='{self.model.contact.URL}'>{self.model.contact.NAME}</a> 2023"
            "\n\nОгромная благодарность за иконки: \n\n"
            '<a href="https://www.flaticon.com/authors/freepik">freepik</a>\n\n'
            '<a href="https://www.svgrepo.com">svgrepo.com</a>\n\n'
        )
        central_layout.addWidget(text_widget)
        modal.exec()

    def menu_settings_button_clicked(self):
        point = self.ui.menu_settings_button.rect().topLeft()
        point.setY(point.y() - (self.ui.context_menu.height() + self.ui.menu_settings_button.height()))
        self.ui.context_menu.exec(self.ui.menu_settings_button.mapToGlobal(point))

    def closeEvent(self, event):
        self.scheduler.pause()
        self.controller.close()
        event.accept()

    def error_handler(self, error):
        self.widgets_factory.message_box(
            "Ошибка",
            "info",
            error,
        ).exec()
