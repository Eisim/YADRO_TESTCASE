import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from typing import Dict, Any

from DataModels.BaseModel import BaseModel
from DataModels import UMLDataClassModel


class XMLConfigModel(BaseModel):
    def __build_hierarchy(self, graph, root):
        hierarchy = {root: {}}
        queue = deque([(root, hierarchy[root])])
        while queue:
            current_node, current_dict = queue.popleft()
            for child in graph.get(current_node, []):
                current_dict[child] = {}
                queue.append((child, current_dict[child]))
        return hierarchy

    def __dict_to_xml(self, content, data: Dict[str, Any], parent=None) -> ET.Element:
        def add_additional_info(xml_elem: ET.Element, class_data: UMLDataClassModel.Class):
            for attr_list in class_data.attribute:
                elem_attrs = ET.SubElement(xml_elem, attr_list.name)
                elem_attrs.text = attr_list.type

        if parent is None:
            root_name = list(data.keys())[0]
            root = ET.Element(root_name)
            data_attrs = content.get_class_by_name(root_name)
            add_additional_info(root, data_attrs)
            self.__dict_to_xml(content, data[root_name], root)
            return root
        else:
            for name, children in data.items():
                elem = ET.SubElement(parent, name)
                data_attrs = content.get_class_by_name(name)
                add_additional_info(elem, data_attrs)

                if children:
                    self.__dict_to_xml(content, children, elem)

    def to_format(self, content: UMLDataClassModel.UMLDataClass) -> ET.Element:
        root_class = next((cls for cls in content.Classes if cls.isRoot), None)
        graph = defaultdict(list)
        for aggr in content.Aggregations:
            graph[aggr.target].append(aggr.source)
        hierarchy = self.__build_hierarchy(graph, root_class.name)
        xml_root = self.__dict_to_xml(content, hierarchy)
        return xml_root
