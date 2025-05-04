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


UMLRENAME_RULE = {
    'name': 'Class',
    'Attribute': 'parameters'
}


class UMLParser(BaseModel):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)
        self.structure = UMLStructure([], [])
        self.__parse()
        _ = self.to_dict()
        self.save_json(_, 'test')

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
        tree = ET.parse(self.path_to_data)
        root = tree.getroot()
        self.structure = UMLStructure(**self.__collect_attributes(root, self.structure))

    def to_dict(self) -> Dict:
        return self.structure.to_dict()

    # FIXME: make it more universal and faster(use hash table[dict] to fast search)
    def dict_to_meta_json_format(self, input_data):
        meta_data = []

        for cls in input_data['Classes']:
            meta_dict = cls
            meta_dict['parameters'] = meta_dict.pop('attribute')
            meta_dict['parameters'] += [{'name': attr_name['source'], 'type': 'class'} for attr_name in
                                        input_data['Aggregations'] if attr_name['target'] == cls['name']]
            multiplicity_arr = [x['sourceMultiplicity'] for x in input_data['Aggregations'] if x['source']==cls['name']]
            if len(multiplicity_arr)!=0:
                meta_dict['min'] = min([x.split('..')[0] for x in multiplicity_arr])
                meta_dict['max'] = max([x.split('..')[-1] for x in multiplicity_arr])

            meta_data.append(meta_dict)
        return meta_data
