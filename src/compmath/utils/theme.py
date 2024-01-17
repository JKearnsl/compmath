import os
import sys
import importlib

from compmath import themes
from compmath.themes.base import BaseTheme

__FOLDER = os.path.dirname(os.path.abspath(themes.__file__))
__DIRNAME = os.path.basename(__FOLDER)


def is_theme(theme_class: type) -> bool:
    try:
        getattr(theme_class, "__title__")
        getattr(theme_class, "__author__"),
        getattr(theme_class, "__version__"),
        getattr(theme_class, "__description__"),
        getattr(theme_class, "first_background"),
        getattr(theme_class, "second_background"),
        getattr(theme_class, "third_background"),
        getattr(theme_class, "primary"),
        getattr(theme_class, "hover"),
        getattr(theme_class, "text_header"),
        getattr(theme_class, "text_primary"),
        getattr(theme_class, "text_secondary")

        return True
    except AttributeError:
        return False


def get_themes() -> tuple[dict[str, tuple[type[BaseTheme], str, str]], list[tuple[str, str]]]:
    items = os.listdir(__FOLDER)

    normal_themes = dict()
    error_themes = list()
    for filename in items:
        if (
                os.path.isfile(os.path.join(__FOLDER, filename)) and
                not filename.startswith("__") and
                filename.endswith(".py") and
                filename != "base.py"
        ):
            module_name = f"{os.path.basename(__FOLDER)}.{filename.replace('.py', '')}"
            module_path = os.path.join(__FOLDER, filename)
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)

                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                is_found_theme_class = False
                for el in dir(module):
                    if not el.startswith("__"):
                        theme_class = getattr(module, el)
                        if (
                                isinstance(theme_class, type) and
                                theme_class != BaseTheme and
                                issubclass(theme_class, BaseTheme) and
                                is_theme(theme_class) and
                                normal_themes.get(theme_class.__title__) is None
                        ):
                            normal_themes[theme_class.__title__] = (theme_class, module_name, module_path)
                            is_found_theme_class = True
                            break

                if is_found_theme_class:
                    continue
                else:
                    error_themes.append((module_name, "Not found theme class"))
            except ModuleNotFoundError:
                error_themes.append((module_name, "Theme loading error"))
            except (AttributeError, TypeError):
                error_themes.append((module_name, "Incorrect theme"))

    return normal_themes, error_themes
