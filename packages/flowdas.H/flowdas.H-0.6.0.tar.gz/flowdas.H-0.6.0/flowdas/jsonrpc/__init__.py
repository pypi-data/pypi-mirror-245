import asyncio
import importlib.metadata
import inspect
import json

from typeable.typing import (
    Any,
    Literal,
    Type,
    Union,
    get_type_hints,
)
from typeable import cast, Object, field, Context, dumps, JsonSchema

from . import openrpc

__version__ = importlib.metadata.version('flowdas.H')


class JsonRpcRequest(Object):
    jsonrpc: Literal['2.0']
    method: str = field(required=True)
    params: Union[dict[str, Any], list] = field(default_factory=dict)
    id: Union[int, str, None]


_FIELD = '_jsonrpc'
_NAME = '_jsonrpc_name'
_UNPACK = '_jsonrpc_unpack'


class Session:
    _rpcs = {}

    def __init__(self, root_class):
        self._services = {}
        rpc = self._rpcs.get(root_class)
        if rpc is None:
            rpc = self._rpcs[root_class] = JsonRpc(root_class)
        self._rpc = rpc

    @property
    def rpc(self) -> 'JsonRpc':
        return self._rpc

    def get_service(self, service_class: Type['Service']) -> 'Service':
        service = self._services.get(service_class)
        if service is None:
            self._services[service_class] = service = service_class(self)
        return service


class Service:
    _methods_ = None
    _name_ = None

    def __init__(self, session: Session):
        self.__session = session

    def __init_subclass__(cls, *, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._name_ = name

    @property
    def session(self):
        return self.__session


def jsonrpc(_=None, *, name=None):
    def deco(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError
        sig = inspect.signature(func)
        hints = get_type_hints(func)
        params = []
        it = iter(sig.parameters.items())
        next(it)  # remove self
        var_pos_arg = None
        sig_args = []
        Parameter = inspect.Parameter
        for key, val in it:
            param = openrpc.ContentDescriptor()
            param.name = key
            tp = hints.get(key, Any)
            if val.default == val.empty:
                param.required = True
            if val.kind == val.VAR_POSITIONAL:
                tp = list[tp]
                var_pos_arg = key
            elif val.kind == val.VAR_KEYWORD:
                tp = dict[str, tp]
            param.schema = JsonSchema(tp)
            params.append(param)
            sig_args.append((key, val.kind, val.default))
        result = openrpc.ContentDescriptor()
        tp = hints.get('return', Any)
        result.name = 'return'
        result.schema = JsonSchema(tp)
        m = openrpc.Method()
        m.params = params
        m.result = result

        def unpack(params, ctx):
            if isinstance(params, dict):
                args, kwargs = [], params
                has_var_pos = bool(kwargs.get(var_pos_arg))
                for key, kind, default in sig_args:
                    with ctx.traverse(key):
                        if kind == Parameter.POSITIONAL_ONLY or kind == Parameter.POSITIONAL_OR_KEYWORD:
                            if kind == Parameter.POSITIONAL_OR_KEYWORD and not has_var_pos:
                                break
                            if key in kwargs:
                                args.append(kwargs.pop(key))
                            elif default != Parameter.empty:
                                args.append(default)
                            else:
                                raise TypeError(
                                    f"{m.name}() missing required positional argument: '{key}'")
                        elif kind == Parameter.VAR_POSITIONAL:
                            args.extend(kwargs.pop(key, []))
                        elif kind == Parameter.VAR_KEYWORD:
                            arg = kwargs.pop(key, None)
                            if arg is not None:
                                conflicts = list(kwargs.keys() & arg.keys())
                                if conflicts:
                                    with ctx.traverse(conflicts[0]):
                                        raise TypeError(
                                            f"{m.name}() got multiple values for argument '{conflicts[0]}'")
                                kwargs.update(arg)
                return args, kwargs
            else:
                # should be list
                args, kwargs = [], {}
                kwd_start = None
                if len(params) > len(sig_args):
                    raise TypeError(
                        f"{m.name}() takes {len(sig_args)} arguments but {len(params)} were given")
                for i, arg in enumerate(params):
                    key, kind, default = sig_args[i]
                    if kind == Parameter.POSITIONAL_ONLY or kind == Parameter.POSITIONAL_OR_KEYWORD:
                        args.append(arg)
                    elif kind == Parameter.VAR_POSITIONAL:
                        args.extend(arg)
                        kwd_start = i + 1
                        break
                    else:
                        kwd_start = i
                        break
                if kwd_start is not None:
                    for i in range(kwd_start, len(params)):
                        key, kind, default = sig_args[i]
                        if kind == Parameter.KEYWORD_ONLY:
                            kwargs[key] = params[i]
                        else:  # VAR_KEYWORD
                            arg = params[i]
                            conflicts = list(kwargs.keys() & arg.keys())
                            if conflicts:
                                with ctx.traverse(conflicts[0]):
                                    raise TypeError(
                                        f"{m.name}() got multiple values for argument '{conflicts[0]}'")
                            kwargs.update(arg)
                return args, kwargs

        setattr(func, _FIELD, m)
        setattr(func, _NAME, name)
        setattr(func, _UNPACK, unpack)
        return func

    return deco if _ is None else deco(_)


class JSONRPCError(Exception):
    def __init__(self, code: int, message, data=None):
        super().__init__(code, message, data)


class JSONRPCParseError(JSONRPCError):
    def __init__(self, data):
        super().__init__(code=-32700, message='Parse error', data=data)


class JSONRPCInvalidRequestError(JSONRPCError):
    def __init__(self, location):
        super().__init__(code=-32600, message='Invalid Request', data=location)


class JSONRPCMethodNotFoundError(JSONRPCError):
    def __init__(self):
        super().__init__(code=-32601, message='Method not found')


class JSONRPCInvalidParamsError(JSONRPCError):
    def __init__(self, location):
        super().__init__(code=-32602, message='Invalid params', data=location)


class JSONRPCInternalError(JSONRPCError):
    def __init__(self):
        super().__init__(code=-32603, message='Internal error')


class JSONRPCValueError(JSONRPCInvalidParamsError):
    def __init__(self, argname):
        super().__init__(f'/params/{argname}')


class JsonRpc:
    def __init__(self, root_class):
        if not hasattr(root_class, 'rpc'):
            root_class.rpc = RpcService
        self._root_class = root_class
        self._dispatch_map = self._build_dispatch_map()

    def get_dispatch_map(self):
        return self._dispatch_map

    def _build_dispatch_map(self):
        dm = {}
        memo = {self}

        def walk(node, prefix):
            memo.add(node)
            for key, val in inspect.getmembers(node, inspect.iscoroutinefunction):
                if isinstance(getattr(val, _FIELD, None), openrpc.Method):
                    dm[f'{prefix}{getattr(val, _NAME, None) or key}'] = node, cast.function(val, keep_async=False)

            for key, val in inspect.getmembers(node, inspect.isclass):
                if issubclass(val, Service):
                    if val in memo:
                        continue
                    name = val._name_ or key
                    walk(val, f'{prefix}{name}.')

        walk(self._root_class, '')
        return dm

    async def dispatch(self, session, data):
        try:
            data = json.loads(data)
        except Exception as e:
            return self._make_error_response(JSONRPCParseError(str(e)), None)
        ctx = Context()
        try:
            with ctx.capture() as err:
                request = cast(JsonRpcRequest, data, ctx=ctx)
        except Exception as e:
            return self._make_error_response(JSONRPCInvalidRequestError(err.location), None)
        # check notification
        has_id = hasattr(request, 'id')
        if not has_id:
            request.id = None
        try:
            pair = self._dispatch_map.get(request.method)
            if not pair:
                raise JSONRPCMethodNotFoundError()
            service_class, method = pair
            service = session.get_service(service_class)
            try:
                with ctx.capture() as err:
                    args, kwargs = getattr(method, _UNPACK)(request.params, ctx)
                    awaitable = method(service, *args, **kwargs)
            except Exception as e:
                raise JSONRPCInvalidParamsError(err.location) from e
            if has_id:
                result = await awaitable
                return dumps({
                    'jsonrpc': '2.0',
                    'result': result,
                    'id': request.id,
                })
            else:
                asyncio.create_task(awaitable)
                return ''
        except Exception as e:
            if has_id:
                return self._make_error_response(e, request.id)
            else:
                return ''

    def _make_error_response(self, e, id):
        if isinstance(e, JSONRPCError):
            code, message, data = e.args
            error = {
                'code': code,
                'message': message,
            }
            if data is not None:
                error['data'] = data
        else:
            error = {
                'code': -32603,
                'message': 'Internal error',
                'data': str(e),
            }
        return json.dumps({
            'jsonrpc': '2.0',
            'error': error,
            'id': id,
        }, ensure_ascii=False, separators=(',', ':'))


class RpcService(Service):
    _schema = None

    @jsonrpc
    async def discover(self) -> openrpc.Document:
        if self._schema is None:
            info = openrpc.Info()
            info.title = 'flowdas'
            info.version = __version__
            methods = []
            dm = self.session.rpc.get_dispatch_map()
            for key, (service_class, val) in dm.items():
                method = getattr(val, _FIELD)
                method.name = key
                methods.append(method)
            doc = openrpc.Document()
            doc.openrpc = openrpc.version
            doc.info = info
            doc.methods = methods
            self._schema = doc
        return self._schema


__all__ = [
    'Service',
    'jsonrpc',
    'JSONRPCValueError',
]
