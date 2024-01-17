from compmath.themes.base import BaseTheme


class DefaultTheme(BaseTheme):

    __title__ = "default"
    __author__ = "JKearnsl"
    __version__ = "0.0.1"
    __description__ = "Тема по умолчанию в строгом стиле"

    first_background: str = "#ffffff"
    second_background: str = "#F5F5F5"
    third_background: str = "#5859BC"
    primary: str = "#2675BF"
    hover: str = "#E0E0E0"
    text_header: str = "#010000"
    text_primary: str = "#010000"
    text_secondary: str = "#909fa6"
    text_tertiary: str = "#ffffff"
