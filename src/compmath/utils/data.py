from dataclasses import fields
from typing import Type, List, Any


def dict_to_dataclass(d: dict, cls: Type) -> object:
    cls_fields = {f.name for f in fields(cls)}
    if set(d.keys()) == cls_fields:
        return cls(**d)
    else:
        raise ValueError(f"The dictionary keys {d.keys()} do not match the fields of {cls}")


def dicts_to_dataclasses(dict_list: List[dict], classes: list) -> List[Any]:
    result = []
    for d in dict_list:
        for cls in classes:
            try:
                instance = dict_to_dataclass(d, cls)
                result.append(instance)
                break
            except ValueError:
                pass
        else:
            raise ValueError(f"No matching data class found for dictionary {d}")
    return result
