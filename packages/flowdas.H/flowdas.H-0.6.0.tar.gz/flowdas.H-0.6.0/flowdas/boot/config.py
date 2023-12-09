import pathlib

import yaml
from typeable import Object, cast
from typeable.typing import Any, Type
from dataclasses import MISSING

_params = {}


def define(name: str, type: Type, default: Any = MISSING):
    _params[name] = (type, default)


class Config(Object):
    
    _loading = False

    @classmethod
    def _load(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        return cast(cls, data)

    @classmethod
    def get_instance(cls, path='f.yaml'):
        instance = getattr(cls, '_instance', None)
        if instance is None:
            if cls._loading:
                raise RuntimeError('Inconsistent Config state')
            path = pathlib.Path(path)
            instance = Config._instance = cls._load(path) if path.exists() else cls()
            cls._home = path.parent.absolute()
        return instance

    @property
    def home(self):
        return self._home

    @property
    def distribution(self):
        return 'flowdas.H'
