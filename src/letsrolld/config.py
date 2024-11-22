import json


class Config:
    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, key):
        return None


def from_file(filename):
    try:
        with open(filename) as f:
            data = json.load(f)
        for name, settings in data.items():
            yield Config(name, **settings)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON file: {e}")
