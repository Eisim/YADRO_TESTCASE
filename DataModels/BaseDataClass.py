from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict


@dataclass
class BaseDataClass:
    @classmethod
    def get_field_info(cls):
        return [(f.name, f.type) for f in fields(cls)]

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    def items(self):
        for field in fields(self):
            yield field.name, getattr(self, field.name)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        if not is_dataclass(self):
            return self

        result = {}
        for field in fields(self):
            value = getattr(self, field.name)

            if is_dataclass(value):
                result[field.name] = value.to_dict()
            elif isinstance(value, list):
                result[field.name] = [item.to_dict() if is_dataclass(item) else item
                                      for item in value]
            elif isinstance(value, dict):
                result[field.name] = {
                    k: v.to_dict() if is_dataclass(v) else v
                    for k, v in value.items()
                }
            else:
                result[field.name] = value

        return result