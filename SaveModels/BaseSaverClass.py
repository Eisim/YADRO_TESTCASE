import json
import xml.etree.ElementTree as ET
from typing import Dict, AnyStr, List
from xml.dom import minidom


class BaseSaveClass:
    def __init__(self):
        pass

    @staticmethod
    def save_json(data: Dict | List[Dict], name: AnyStr) -> None:
        file_name = name if name.split('.')[-1] == 'json' else name + '.json'
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def save_xml(data: ET.Element, name: AnyStr) -> None:
        file_name = name if name.split('.')[-1] == 'xml' else name + '.xml'

        xml_str = ET.tostring(data, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")
        with open(file_name, 'w') as f:
            f.write(pretty_xml)
