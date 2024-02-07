from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor
from PyQt6.QtWidgets import QWidget, QTableView, QHeaderView


class Matrix(QTableView):
    itemChanged = pyqtSignal(QStandardItem)

    def __init__(
            self,
            primary_text_color: str,
            selection_color: str,
            hover_color: str,
            background_color: str,
            parent: QWidget = None
    ):
        super().__init__(parent)

        self.is_hidden_b = False
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setModel(QStandardItemModel(0, 0))
        self._hover_color = hover_color

        self.setStyleSheet("""
            QTableView {
                border: 2px solid $HOVER;
                border-radius: 5px;
                background: $BG3;
                color: $PRIMARY_TEXT_COLOR;
            }
            QTableView:disabled {
                background: $HOVER;
            }
            QTableView::item {
                padding: 5px;
            }
            QTableView::item:selected {
                background: $SELECTION;
                color: $PRIMARY_TEXT_COLOR;
            }
            QTableView::item:hover {
                background: $HOVER;
                color: $PRIMARY_TEXT_COLOR;
            }

            QHeaderView::section {
                background: $BG3;
                color: $PRIMARY_TEXT_COLOR;
                padding: 5px;
                border-bottom: 2px solid $HOVER;
            }
            QHeaderView::section:hover {
                background: $HOVER;
            }

            QScrollBar:vertical {
                border: none;
                background: $BG3;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: $HOVER;
                border-radius: 2px;
                min-height: 0px;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """.replace(
            "$SELECTION", selection_color
        ).replace(
            "$PRIMARY_TEXT_COLOR", primary_text_color
        ).replace(
            "$HOVER", hover_color
        ).replace(
            "$BG3", background_color
        ))

        self.model().itemChanged.connect(self.itemChanged.emit)

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)

    def a(self) -> list[list[[float | int]]]:
        matrix = []
        for i in range(self.model().rowCount()):
            for j in range(self.model().columnCount()):
                matrix.append(self.model().data(self.model().index(i, j)))
        return matrix

    def b(self) -> list[float | int]:
        values = []
        if not self.is_hidden_b:
            for i in range(self.model().rowCount()):
                values.append(self.model().data(self.model().index(i, self.model().columnCount())))
        return values

    def matrix(self) -> list[list[float | int]]:
        ...

    def set_a(self, matrix: list[list[float | int]]) -> None:
        b_matrix = self.b()
        if b_matrix and len(b_matrix) != len(matrix):
            delta = abs(len(b_matrix) - len(matrix))
            if len(b_matrix) < len(matrix):
                b_matrix.extend([0] * delta)
            else:
                b_matrix = b_matrix[:len(matrix)]

        self.model().setRowCount(len(matrix))
        if matrix:
            self.model().setColumnCount(len(matrix[0]) + (1 if b_matrix else 0))

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                value = matrix[i][j]
                item = QStandardItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.model().setItem(i, j, item)

        if b_matrix:
            for i, value in enumerate(b_matrix):
                item = QStandardItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.model().setItem(i, len(matrix[0]), item)

    def set_b(self, values: list[float | int]) -> None:
        b_matrix = self.b()
        a_matrix = self.a()

        self.model().setRowCount(len(values))
        if not b_matrix:
            self.model().setColumnCount(len(a_matrix) + 1)

        if a_matrix and len(a_matrix[0]) < len(values):
            for row_index in range(len(a_matrix), len(values)):
                for col_index in range(len(a_matrix[0])):
                    item = QStandardItem("0")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.model().setItem(row_index, col_index, item)

        for row_index, value in enumerate(values):
            item = QStandardItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(QColor(self._hover_color))
            self.model().setItem(row_index, self.model().columnCount() - 1, item)
