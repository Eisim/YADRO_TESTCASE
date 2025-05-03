from BaseModel import BaseModel


class ConfigModel(BaseModel):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)
