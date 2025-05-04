import json
import xml.etree.ElementTree as ET
from xml.dom import minidom


class BaseModel:
    def __init__(self, path_to_data):
        self.path_to_data = path_to_data
    def save_json(self, dict_data, name):
        file_name = name if name.split('.')[-1] == 'json' else name + '.json'
        with open(file_name, 'w') as f:
            json.dump(dict_data, f, ensure_ascii=False, indent=4)
    def save_xml(self, data, name):
        file_name = name if name.split('.')[-1] == 'xml' else name + '.xml'

        xml_str = ET.tostring(data, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")
        with open(file_name,'w') as f:
            f.write(pretty_xml)
