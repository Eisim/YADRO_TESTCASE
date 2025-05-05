import xml.etree.ElementTree as ET
from typing import get_origin, get_args, AnyStr

from DataModels.UMLDataClassModel import UMLDataClass
from FileReaders.BaseFileReader import BaseFileReader
from settings import COLLECTION_TYPES


class UMLReaderClass(BaseFileReader):
    @classmethod
    def __collect_attributes(cls, xml_element, obj_type):
        attr_data = {}
        for attr_name, attr_type in obj_type.get_field_info():
            if get_origin(attr_type) in COLLECTION_TYPES:
                obj_collection = []
                for collection_type in get_args(attr_type):
                    collection_type_name = collection_type.get_class_name()
                    obj_collection += [collection_type(**cls.__collect_attributes(xml_child, collection_type)) for
                                       xml_child in
                                       xml_element.findall(collection_type_name)]
                attr_data[attr_name] = obj_collection
            else:
                attr_data[attr_name] = xml_element.get(attr_name)
        return attr_data

    def read(self, path: AnyStr):
        tree = ET.parse(path)
        root = tree.getroot()
        content = UMLDataClass(**self.__collect_attributes(root, UMLDataClass))
        return content
