import xml.etree.ElementTree as ET
import json

from dataclasses import dataclass, fields, is_dataclass
from typing import Dict, List, get_args, get_origin, Any

from BaseModel import BaseModel
from settings import COLLECTION_TYPES


@dataclass
class BaseDataClass:
    @classmethod
    def get_field_info(cls):
        return [(f.name, f.type) for f in fields(cls)]

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Рекурсивно преобразует объект dataclass в словарь"""
        if not is_dataclass(self):
            return self

        result = {}
        for field in fields(self):
            value = getattr(self, field.name)

            # Рекурсивная обработка вложенных объектов
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


@dataclass
class Attribute(BaseDataClass):
    name: str
    type: str


@dataclass
class Class(BaseDataClass):
    name: str
    isRoot: bool
    documentation: str
    attribute: List[Attribute]


@dataclass
class Aggregation(BaseDataClass):
    source: str
    target: str
    sourceMultiplicity: str
    targetMultiplicity: str


@dataclass
class UMLStructure(BaseDataClass):
    Classes: List[Class]
    Aggregations: List[Aggregation]


class UMLParser(BaseModel):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)
        self.structure = UMLStructure([], [])
        self.__parse()
        self.to_dict()

    def __collect_attributes(self, xml_element, obj_type):
        attr_data = {}
        for attr_name, attr_type in obj_type.get_field_info():
            if get_origin(attr_type) in COLLECTION_TYPES:
                obj_collection = []
                for collection_type in get_args(attr_type):
                    collection_type_name = collection_type.get_class_name()
                    obj_collection += [self.__collect_attributes(xml_child, collection_type) for xml_child in
                                       xml_element.findall(collection_type_name)]
                attr_data[attr_name] = obj_collection
            else:
                attr_data[attr_name] = xml_element.get(attr_name)
        return attr_data

    def __parse(self) -> None:
        tree = ET.parse(self.path_to_model)
        root = tree.getroot()

        # FIXME: for ... for .. for ... -> recursive alg
        for obj_name, list_type in self.structure.get_field_info():
            if get_origin(list_type) in [list, tuple]:
                for obj_type in get_args(list_type):
                    obj_type_class_name = obj_type.get_class_name()
                    for xml_element in root.findall(obj_type_class_name):
                        cur_obj = self.__collect_attributes(xml_element, obj_type)
                        self.structure[obj_name].append(obj_type(**cur_obj))

    def to_dict(self) -> Dict:
        return self.structure.to_dict()

    def save_json(self, dict_data, name):
        file_name = name if name.split('.')[1] == 'json' else name + '.json'
        with open(file_name, 'w') as f:
            json.dump(self.structure.to_dict(), f, ensure_ascii=False, indent=4)
