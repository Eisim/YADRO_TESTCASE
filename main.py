from ConfigParser import ConfigParser
from UMLParser import UMLParser




if __name__ == '__main__':
    xml_model = UMLParser(r'input/impulse_test_input.xml')

    res_dict = xml_model.dict_to_meta_json_format(xml_model.to_dict())
    xml_model.save_json(xml_model.to_dict(),'test_2')
    xml_model.save_json(res_dict,'out/meta.json')

    cfg_parser = ConfigParser(path_to_data='input/config.json',path_to_patched_data =r'input/patched_config.json')

    cfg_parser.save_json(cfg_parser.diff_struct,"out/delta.json")
    cfg_parser.save_json(cfg_parser.new_struct,'out/res_patched_config.json')