import json
from typing import AnyStr, Dict

from FileReaders.BaseFileReader import BaseFileReader


class JSONReaderClass(BaseFileReader):
    def read(self, path: AnyStr) -> Dict:
        with open(path, 'r') as f:
            return json.load(f)
