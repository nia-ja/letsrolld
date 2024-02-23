from decimal import Decimal
import json


_DEFAULT_NUM_MOVIES = 5
_DEFAULT_NUM_MOVIES_PER_DIRECTOR = 3
_DEFAULT_MIN_LENGTH = 0
_DEFAULT_MAX_LENGTH = 240


class Config:
    def _set_defaults(self):
        self.max_movies = self.max_movies or _DEFAULT_NUM_MOVIES
        self.max_movies_per_director = self.max_movies_per_director or _DEFAULT_NUM_MOVIES_PER_DIRECTOR
        self.min_length = self.min_length or _DEFAULT_MIN_LENGTH
        self.max_length = self.max_length or _DEFAULT_MAX_LENGTH

    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._set_defaults()

    def __setattr__(self, key, value):
        if key in ("min_rating", "max_rating"):
            if value is not None:
                value = Decimal(value)
        elif key in ("min_length", "max_length"):
            if value is not None:
                value = int(value)
        elif key in ("text",):
            if value is not None:
                value = value.lower()
        super().__setattr__(key, value)

    def __getattr__(self, key):
        return None

    @classmethod
    def from_file(cls, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for name, settings in data.items():
                    yield Config(name, **settings)
        except FileNotFoundError:
            raise
        except json.JSONDecodeError as e:
            raise ValueError(f"invalid JSON file: {e}")
