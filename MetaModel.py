
from collections import deque, defaultdict
from typing import Dict, Any

import UMLDataClassModel
from base_classes.BaseModel import BaseModel




class MetaModel(BaseModel):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)

    def to_format(self, content: UMLDataClassModel):
        content = content.to_dict()
        meta_data = []

        for cls in content['Classes']:
            meta_dict = cls
            meta_dict['parameters'] = meta_dict.pop('attribute')
            meta_dict['parameters'] += [{'name': attr_name['source'], 'type': 'class'} for attr_name in
                                        content['Aggregations'] if attr_name['target'] == cls['name']]
            multiplicity_arr = [x['sourceMultiplicity'] for x in content['Aggregations'] if
                                x['source'] == cls['name']]
            if len(multiplicity_arr) != 0:
                meta_dict['min'] = min([x.split('..')[0] for x in multiplicity_arr])
                meta_dict['max'] = max([x.split('..')[-1] for x in multiplicity_arr])

            meta_data.append(meta_dict)
        return meta_data