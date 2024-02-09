from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QListView

from compmath.utils.icon import svg_ico


class List(QListView):
    def __init__(
            self,
            hover_color,
            selected_text_color,
            selected_color,
            text_color,
            parent=None
    ):
        super().__init__(parent)

        self.setStyleSheet("""
            QListView {
                background-color: transparent;
                selection-background-color: transparent;
                outline: none;
                font-size: 13px;
                color: $TEXT_NORMAL;
            }
            QListView::item {
                border: none;
                padding-left: 10px;
            }
            QListView::item:hover {
                background-color: $HOVER;
            }
            QListView::item:selected {
                background: $SELECTION;
                color: $TEXT_SELECTED;
            }
                """.replace(
            "$TEXT_SELECTED", selected_text_color
        ).replace(
            "$HOVER", hover_color
        ).replace(
            "$SELECTION", selected_color
        ).replace(
            "$TEXT_NORMAL", text_color
        ))
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setMovement(QtWidgets.QListView.Movement.Static)
        self.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.setResizeMode(QtWidgets.QListView.ResizeMode.Fixed)
        self.setSpacing(0)
        self.setUniformItemSizes(True)
        self.setWordWrap(False)
        self.setWrapping(False)
        self.setMouseTracking(True)
        self.setTabKeyNavigation(False)
        self.setFrameStyle(0)

        self.setModel(QtGui.QStandardItemModel())

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)


class ListItemWidget(QtGui.QStandardItem):
    id: any

    def __init__(self, title: str, _id: any = None, svg_icon_path: str = None):
        super().__init__()
        self.setText(title)
        self.id = _id
        self.svg_icon_path = svg_icon_path
        self.setSizeHint(QtCore.QSize(0, 40))

    def set_icon_color(self, color: str):
        if self.svg_icon_path:
            self.setIcon(svg_ico(self.svg_icon_path, color))

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} title={self.text()}>"
