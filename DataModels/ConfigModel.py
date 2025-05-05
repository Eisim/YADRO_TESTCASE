import json
from typing import Dict, Any, AnyStr

from DataModels.BaseModel import BaseModel


class ConfigModel(BaseModel):
    @staticmethod
    def compare_cfg(old_config: Dict[AnyStr, Any], new_config: Dict[Any, AnyStr]) -> Dict[AnyStr, Any]:
        additions = []
        deletions = []
        updates = []
        new_keys = set(new_config.keys())
        for k, v in old_config.items():
            if k not in new_config:
                deletions.append(k)
            elif k in new_config and v != new_config[k]:
                updates.append({
                    "key": k,
                    "from": v,
                    "to": new_config[k]
                })
            if k in new_config:
                new_keys.remove(k)
        for k in new_keys:
            additions.append({
                "key": k,
                "value": new_config[k]
            })
        return {
            "additions": additions,
            "deletions": deletions,
            "updates": updates
        }

    @staticmethod
    def apply_delta_to_config(base_config: Dict[AnyStr, Any], delta_dict: Dict[AnyStr, Any]) -> Dict[AnyStr, Any]:
        new_dict = base_config.copy()
        for key in delta_dict.get('deletions', []):
            new_dict.pop(key, None)
        for update in delta_dict.get('updates', []):
            if update['key'] in new_dict and new_dict[update['key']] == update['from']:
                new_dict[update['key']] = update['to']
        for addition in delta_dict.get('additions', []):
            new_dict[addition['key']] = addition['value']
        return new_dict
