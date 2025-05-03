from ConfigParser import ConfigParser
from UMLParser import UMLParser


class App:
    def __init__(self, xml_model: UMLParser, config: ConfigParser, patched_config: ConfigParser):
        self.input_xml = xml_model
        self.config = config
        self.patched_config = patched_config


if __name__ == '__main__':
    xml_model = UMLParser(r'input/impulse_test_input.xml')

    res_dict = xml_model.dict_to_task_format(xml_model.to_dict())
    xml_model.save_json(res_dict,'test_2')


    cfg_parser = ConfigParser(path_to_data='input/config.json',path_to_patched_data =r'input/patched_config.json')

    cfg_parser.save_json(cfg_parser.diff_struct,"out/delta.json")
    cfg_parser.save_json(cfg_parser.new_struct,'out/res_patched_config.json')