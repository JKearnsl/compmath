"""
Модуль реализации мета класса, необходимого для работы представления.

pyqtWrapperType - мета класс общий для оконных компонентов Qt.
ABCMeta - мета класс для реализации абстрактных супер классов.

TSMeta - мета класс для представления.
"""

from PyQt6.QtCore import QObject
from abc import ABCMeta


class TSMeta(type(QObject), ABCMeta):
    pass
