from typing import Any


class BaseFileReader:
    def __init__(self):
        pass

    def read(self, path: str) -> Any:
        with open(path, 'r') as f:
            return f.read()
