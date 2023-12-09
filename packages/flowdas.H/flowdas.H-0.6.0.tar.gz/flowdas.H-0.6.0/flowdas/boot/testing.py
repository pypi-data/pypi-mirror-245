import pytest

from .main import load_config


@pytest.fixture
def config():
    return load_config()


__all__ = [
    'config',
]
