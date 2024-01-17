from typing import TypeVar, Literal

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget

from compmath.themes.base import BaseTheme
from compmath.views.widgets.button import Button
from compmath.views.widgets.button_outline import ButtonOutline
from compmath.views.widgets.combo_box import ComboBox
from compmath.views.widgets.dialog import Dialog
from compmath.views.widgets.double_spin_box import DoubleSpinBox
from compmath.views.widgets.graphic import Graphic
from compmath.views.widgets.heading import Heading1
from compmath.views.widgets.heading import Heading2
from compmath.views.widgets.heading import Heading3
from compmath.views.widgets.heading import Heading4
from compmath.views.widgets.heading import Heading5
from compmath.views.widgets.heading import Heading6
from compmath.views.widgets.input_label import InputLabel

from compmath.views.widgets.label import Label
from compmath.views.widgets.line_edit import LineEdit
from compmath.views.widgets.list import List
from compmath.views.widgets.message_box import MessageBox
from compmath.views.widgets.spin_box import SpinBox
from compmath.views.widgets.table import Table
from compmath.views.widgets.textarea import TextArea

QWidgetLike = TypeVar("QWidgetLike", bound=QWidget)


class WidgetsFactory:
    def __init__(self, theme_class: BaseTheme):
        self.theme = theme_class

    def label(self, text: str = None, color: str = None, *, parent: QWidgetLike = None) -> Label:
        lb = Label(
            color if color else self.theme.text_primary,
            parent
        )
        if text:
            lb.setText(text)
        return lb

    def subtitle(self, text: str = None, *, parent: QWidgetLike = None) -> Label:
        lb = Label(self.theme.text_secondary, parent)
        if text:
            lb.setText(text)
        return lb

    def heading1(self, text: str = None, color: str = None, *, parent: QWidgetLike = None) -> Heading1:
        lb = Heading1(
            color if color else self.theme.text_header,
            parent
        )
        if text:
            lb.setText(text)
        return lb

    def heading2(self, text: str = None, *, parent: QWidgetLike = None) -> Heading2:
        lb = Heading2(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading3(self, text: str = None, *, parent: QWidgetLike = None) -> Heading3:
        lb = Heading3(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading4(self, text: str = None, *, parent: QWidgetLike = None) -> Heading4:
        lb = Heading4(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading5(self, text: str = None, *, parent: QWidgetLike = None) -> Heading5:
        lb = Heading5(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading6(self, text: str = None, *, parent: QWidgetLike = None) -> Heading6:
        lb = Heading6(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def combo_box(self, parent: QWidgetLike = None) -> ComboBox:
        return ComboBox(
            selection_color=self.theme.primary,
            primary_text_color=self.theme.text_primary,
            first_background_color=self.theme.first_background,
            second_background_color=self.theme.second_background,
            third_background_color=self.theme.third_background,
            hover_color=self.theme.hover,
            parent=parent
        )

    def spin_box(self, parent: QWidgetLike = None) -> SpinBox:
        return SpinBox(
            selection_color=self.theme.primary,
            primary_text_color=self.theme.text_primary,
            first_background_color=self.theme.first_background,
            second_background_color=self.theme.second_background,
            parent=parent
        )

    def double_spin_box(self, parent: QWidgetLike = None) -> DoubleSpinBox:
        return DoubleSpinBox(
            selection_color=self.theme.primary,
            primary_text_color=self.theme.text_primary,
            first_background_color=self.theme.first_background,
            second_background_color=self.theme.second_background,
            parent=parent
        )

    def modal(self, parent: QWidgetLike = None) -> Dialog:
        return Dialog(
            background_window=self.theme.first_background,
            background_close_btn=self.theme.second_background,
            hover_close_btn=self.theme.hover,
            text_color_close_btn=self.theme.text_header,
            parent=parent
        )

    def message_box(
            self,
            title: str,
            _type: Literal["info", "warning", "error"],
            content: str,
            parent: QWidgetLike = None
    ) -> MessageBox:
        if _type == "info":
            icon = QIcon("icons:info.svg")
        elif _type == "warning":
            icon = QIcon("icons:warning.svg")
        elif _type == "error":
            icon = QIcon("icons:error.svg")
        else:
            raise ValueError("Unknown type")
        _ = MessageBox(
            title=_type.capitalize(),
            content=content,
            icon=icon,
            background_window=self.theme.first_background,
            background_close_btn=self.theme.second_background,
            hover_close_btn=self.theme.hover,
            text_color_close_btn=self.theme.text_header,
            parent=parent
        )
        _.set_title(title)
        return _

    def button(self, text: str = None, *, parent: QWidgetLike = None) -> Button:
        btn = Button(
            self.theme.hover,
            self.theme.first_background,
            self.theme.text_tertiary,
            self.theme.text_primary,
            parent
        )
        if text:
            btn.setText(text)
        return btn

    def primary_button(self, text: str = None, *, parent: QWidgetLike = None) -> Button:
        btn = Button(
            self.theme.hover,
            self.theme.primary,
            self.theme.text_primary,
            self.theme.text_tertiary,
            parent
        )
        if text:
            btn.setText(text)
        return btn

    def outline_button(self, text: str = None, *, parent: QWidgetLike = None) -> ButtonOutline:
        btn = ButtonOutline(
            self.theme.text_tertiary,
            self.theme.hover,
            parent
        )
        if text:
            btn.setText(text)
        return btn

    def list(self, parent: QWidgetLike = None) -> List:
        return List(
            text_primary_color=self.theme.text_primary,
            hover_color=self.theme.hover,
            selection_color=self.theme.primary,
            text_tertiary_color=self.theme.text_tertiary,
            parent=parent
        )

    def line_edit(self, parent: QWidgetLike = None) -> LineEdit:
        return LineEdit(
            selection_color=self.theme.primary,
            primary_text_color=self.theme.text_primary,
            hover_color=self.theme.hover,
            first_background_color=self.theme.first_background,
            parent=parent
        )

    def textarea(self, parent: QWidgetLike = None) -> TextArea:
        return TextArea(
            selection_color=self.theme.primary,
            primary_text_color=self.theme.text_primary,
            hover_color=self.theme.hover,
            background_color=self.theme.first_background,
            parent=parent
        )

    def table(self, parent: QWidgetLike = None) -> Table:
        return Table(
            selection_color=self.theme.primary,
            primary_text_color=self.theme.text_primary,
            hover_color=self.theme.hover,
            third_background_color=self.theme.third_background,
            parent=parent
        )

    def input_label(self, *, parent: QWidgetLike = None) -> InputLabel:
        return InputLabel(
            self.theme.text_primary,
            parent
        )

    def graphic(self, *, parent: QWidgetLike = None) -> Graphic:
        return Graphic(
            self.theme.text_primary,
            self.theme.hover,
            self.theme.second_background,
            parent
        )