from ConfigModel import ConfigModel
from UMLParser import UMLParser


class App:
    def __init__(self, xml_model: UMLParser, config: ConfigModel, patched_config: ConfigModel):
        self.input_xml = xml_model
        self.config = config
        self.patched_config = patched_config


if __name__ == '__main__':
    xml_model = UMLParser(r'input/impulse_test_input.xml')