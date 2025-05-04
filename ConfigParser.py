from BaseModel import BaseModel
import json


class ConfigParser(BaseModel):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)
        with open(self.path_to_data, 'r') as f:
            self.old_struct = json.load(f)
    def read_json(self, path_to_json):
        with open(path_to_json, 'r') as f:
            new_json = json.load(f)
        return new_json
    def compare(self, new_struct):
        additions = []
        deletions = []
        updates = []
        new_keys = set(new_struct.keys())
        for k, v in self.old_struct.items():
            if k not in new_struct:
                deletions.append(k)
            elif k in new_struct and v != new_struct[k]:
                updates.append({
                    "key": k,
                    "from": v,
                    "to": new_struct[k]
                })
            if k in new_struct:
                new_keys.remove(k)
        for k in new_keys:
            additions.append({
                "key": k,
                "value": new_struct[k]
            })
        return {
            "additions": additions,
            "deletions": deletions,
            "updates": updates
        }

    def delta_applying(self, delta_dict):
        new_dict = self.old_struct.copy()
        for key in delta_dict.get('deletions', []):
            new_dict.pop(key, None)
        for update in delta_dict.get('updates', []):
            if update['key'] in new_dict and new_dict[update['key']] == update['from']:
                new_dict[update['key']] = update['to']
        for addition in delta_dict.get('additions', []):
            new_dict[addition['key']] = addition['value']
        return new_dict