from ConfigParser import ConfigParser
from UMLParser import UMLParser
from settings import *

import os

if __name__ == '__main__':


    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    xml_model = UMLParser(os.path.join(INPUT_DIR, IMP_TEST_XML))

    raw_data = xml_model.to_dict()
    meta_json_data = xml_model.dict_to_meta_json_format(raw_data)
    cfg_xml_data = xml_model.struct_to_config_xml()

    xml_model.save_json(meta_json_data, os.path.join(OUTPUT_DIR, META_JSON))
    xml_model.save_xml(cfg_xml_data, os.path.join(OUTPUT_DIR, CFG_XML))

    cfg_parser = ConfigParser(os.path.join(INPUT_DIR, CFG_JSON))

    new_cfg_struct = cfg_parser.read_json(os.path.join(INPUT_DIR, PATCHED_CFG_JSON))
    diff_struct = cfg_parser.compare(new_cfg_struct)
    new_cfg_struct_by_diff = cfg_parser.delta_applying(diff_struct)

    cfg_parser.save_json(diff_struct, os.path.join(OUTPUT_DIR, DELTA_JSON))
    cfg_parser.save_json(new_cfg_struct_by_diff, os.path.join(OUTPUT_DIR, RES_PATCHED_CFG_JSON))
