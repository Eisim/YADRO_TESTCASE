from BaseModel import BaseModel
import json


class ConfigParser(BaseModel):
    def __init__(self, path_to_patched_data, *args, **kvargs):
        super().__init__(*args, **kvargs)
        self.path_to_patched_data = path_to_patched_data
        with open(self.path_to_data, 'r') as f:
            self.old_struct = json.load(f)

        with open(self.path_to_patched_data, 'r') as f:
            self.new_struct = json.load(f)
        self.diff_struct = self.__compare()

    def __compare(self):
        additions = []
        deletions = []
        updates = []
        new_keys = set(self.new_struct.keys())
        for k, v in self.old_struct.items():
            if k not in self.new_struct:
                deletions.append(k)
            elif k in self.new_struct and v != self.new_struct[k]:
                updates.append({
                    "key": k,
                    "from": v,
                    "to": self.new_struct[k]
                })
            if k in self.new_struct:
                new_keys.remove(k)
        for k in new_keys:
            additions.append({
                "key": k,
                "value": self.new_struct[k]
            })
        return {
            "additions": additions,
            "deletions": deletions,
            "updates": updates
        }
