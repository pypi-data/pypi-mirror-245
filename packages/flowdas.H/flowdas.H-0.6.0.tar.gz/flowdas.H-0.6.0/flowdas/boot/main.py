import sys

from .config import Config as BaseConfig, _params, MISSING
from .command import command


@command()
def version():
    try:
        from importlib import metadata
    except ImportError:  # pragma: no cover
        import importlib_metadata as metadata

    cfg = BaseConfig.get_instance()
    v = metadata.version(cfg.distribution)
    print(v)


@command()
def config():
    from typeable import cast, JsonValue
    import pprint
    cfg = BaseConfig.get_instance()
    settings = cast(JsonValue, cfg)
    pprint.pprint(settings)


def load_config():
    BaseConfig._loading = True
    try:
        if sys.version_info < (3, 10):
            from importlib_metadata import entry_points
        else:
            from importlib.metadata import entry_points
        plugins = entry_points(group='flowdas.boot')
        for ep in plugins:
            if ep[0] == 'plugin' or ep[0].startswith('plugin.'):
                ep.load()
        annotations = {}
        attrs = {}
        for name, (tp, default) in _params.items():
            annotations[name] = tp
            if default is not MISSING:
                attrs[name] = default
        if annotations:
            attrs['__annotations__'] = annotations
        Config = type('Config', (BaseConfig,), attrs)
    finally:
        BaseConfig._loading = False
    return Config.get_instance()


def main():
    load_config()

    # cli
    from .command import main
    main()
