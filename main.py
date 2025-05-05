from DataModels.ConfigModel import ConfigModel
from DataModels.MetaModel import MetaModel
from FileReaders.JSONReaderClass import JSONReaderClass
from FileReaders.UMLReaderClass import UMLReaderClass
from DataModels.XMLConfigModel import XMLConfigModel
from SaveModels.BaseSaverClass import BaseSaveClass
from settings import *

import os


class App:
    @staticmethod
    def run():
        uml_model_data = UMLReaderClass().read(os.path.join(INPUT_DIR, IMP_TEST_XML))
        BaseSaveClass.save_json(uml_model_data.to_dict(), 'test')
        json_meta_data = MetaModel().to_format(uml_model_data)
        xml_config_data = XMLConfigModel().to_format(uml_model_data)

        json_old_cfg_data = JSONReaderClass().read(os.path.join(INPUT_DIR, CFG_JSON))
        json_new_cfg_data = JSONReaderClass().read(os.path.join(INPUT_DIR, PATCHED_CFG_JSON))

        json_cfg_delta_data = ConfigModel().compare_cfg(json_old_cfg_data, json_new_cfg_data)
        json_created_new_cfg_data = ConfigModel().apply_delta_to_config(json_old_cfg_data, json_cfg_delta_data)

        path_to_save_meta = os.path.join(OUTPUT_DIR, META_JSON)
        path_to_save_cfg = os.path.join(OUTPUT_DIR, CFG_XML)
        path_to_save_delta = os.path.join(OUTPUT_DIR, DELTA_JSON)
        path_to_save_patched_cfg = os.path.join(OUTPUT_DIR, RES_PATCHED_CFG_JSON)

        BaseSaveClass.save_xml(xml_config_data, path_to_save_cfg)
        BaseSaveClass.save_json(json_meta_data, path_to_save_meta)
        BaseSaveClass.save_json(json_cfg_delta_data, path_to_save_delta)
        BaseSaveClass.save_json(json_created_new_cfg_data, path_to_save_patched_cfg)
        return


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    App.run()
