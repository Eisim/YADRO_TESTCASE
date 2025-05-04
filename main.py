from ConfigParser import ConfigParser
from UMLParser import UMLParser

import os

if __name__ == '__main__':
    # input
    input_dir = './input'
    cfg_json = 'config.json'
    patched_cfg_json = 'patched_config.json'
    imp_test_xml = 'impulse_test_input.xml'
    # output
    output_dir = './out/'
    meta_json = 'meta.json'
    cfg_xml = 'config.xml'
    delta_json = 'delta.json'
    res_patched_cfg_json = 'res_patched_config.json'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    xml_model = UMLParser(os.path.join(input_dir, imp_test_xml))

    raw_data = xml_model.to_dict()
    meta_json_data = xml_model.dict_to_meta_json_format(raw_data)
    cfg_xml_data = xml_model.struct_to_config_xml()

    xml_model.save_json(meta_json_data, os.path.join(output_dir, meta_json))
    xml_model.save_xml(cfg_xml_data, os.path.join(output_dir, cfg_xml))

    cfg_parser = ConfigParser(os.path.join(input_dir, cfg_json))

    new_cfg_struct = cfg_parser.read_json(os.path.join(input_dir, patched_cfg_json))
    diff_struct = cfg_parser.compare(new_cfg_struct)
    new_cfg_struct_by_diff = cfg_parser.delta_applying(diff_struct)

    cfg_parser.save_json(diff_struct, os.path.join(output_dir, delta_json))
    cfg_parser.save_json(new_cfg_struct_by_diff, os.path.join(output_dir, res_patched_cfg_json))
