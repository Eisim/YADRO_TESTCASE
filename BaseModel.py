import json


class BaseModel:
    def __init__(self, path_to_data):
        self.path_to_data = path_to_data
    def save_json(self, dict_data, name):
        file_name = name if len(name.split('.'))==2 and name.split('.')[1] == 'json' else name + '.json'
        with open(file_name, 'w') as f:
            json.dump(dict_data, f, ensure_ascii=False, indent=4)