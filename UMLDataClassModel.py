from base_classes.BaseDataClass import BaseDataClass

from dataclasses import dataclass
from typing import List

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

    def get_class_by_name(self, name):
        return next((cls for cls in self.Classes if cls.name == name), None)