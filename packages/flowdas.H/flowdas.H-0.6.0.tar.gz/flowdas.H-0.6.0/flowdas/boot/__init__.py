import importlib.metadata

__version__ = importlib.metadata.version('flowdas.H')

from .config import Config, define
from .command import command
from . import main

__all__ = [
    'Config',
    'command',
    'define',
]
