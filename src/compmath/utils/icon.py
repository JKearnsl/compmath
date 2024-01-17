import tempfile

from PyQt6.QtCore import QFile
from PyQt6.QtGui import QIcon
from PyQt6.QtXml import QDomDocument


def set_attr_recur(elem, tagname, attr, attr_val):
    if elem.tagName() == tagname:
        elem.setAttribute(attr, attr_val)
    for i in range(elem.childNodes().count()):
        child = elem.childNodes().at(i)
        if child.isElement():
            set_attr_recur(child.toElement(), tagname, attr, attr_val)


def svg_ico(ico_filepath, color='black', attr_color: str = "fill") -> QIcon:
    """
    Создать svg иконку с цветом заливки

    :param ico_filepath: path to any icon file
    :param color: any str color
    :param attr_color: svg attribute name

    :return: QIcon
    """
    file = QFile(ico_filepath)
    file.open(QFile.OpenModeFlag.ReadOnly)
    doc = QDomDocument()
    doc.setContent(file.readAll())
    file.close()

    set_attr_recur(doc.documentElement(), 'path', attr_color, color)

    temp_file = tempfile.NamedTemporaryFile(suffix='.svg', delete=False)
    temp_file.write(doc.toByteArray())
    temp_file.close()

    return QIcon(temp_file.name)
