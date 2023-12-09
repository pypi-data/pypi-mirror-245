from flowdas.boot import command, define
from flowdas.jsonrpc import Service
from typeable import field, Object
from typeable.typing import Type


#
# configuration
#

class Path(Object):
    path: str
    root_class: Type[Service] = Service


define('max_session_rpc_concurrency', int, 16)  # 동시에 실행할 수 있는 세션당 RPC 요청 수
define('paths', list[Path], field(default_factory=lambda: [Path({'path': '/'})]))


#
# commands
#

@command()
def run():
    from .server import Server
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass

    Server().run()


@command()
def shutdown():
    from .server import Server
    Server.notify_shutdown()
