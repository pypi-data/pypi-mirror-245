import functools
import inspect

from falcon import HTTPUnauthorized, HTTPForbidden
from falcon.hooks import _DECORABLE_METHOD_NAME

from flowdas.boot import Config

from . import asgi
from .auth import AuthError, AuthOutcome

_default_security = None
_default_security_deco = None

def _get_default_security():
    global _default_security
    if _default_security is None:
        _default_security = list(Config.get_instance().security or [])
    return _default_security

def _get_default_security_deco():
    global _default_security_deco
    if _default_security_deco is None:
        scopes = _get_default_security()
        _default_security_deco = security(*scopes)
    return _default_security_deco


def route(uri_template):
    def deco(klass):
        if callable(klass):
            inst = klass()
        else:
            inst = klass
            klass = inst.__class__
        for responder_name, responder in inspect.getmembers(klass, callable):
            if _DECORABLE_METHOD_NAME.match(responder_name):
                if not getattr(responder, _MARKER, None):
                    @functools.wraps(responder)
                    async def wrapper(self, req, resp, *args, **kwargs):
                        deco = _get_default_security_deco()
                        wrapped = deco(responder)
                        setattr(klass, responder_name, wrapped)
                        return await wrapped(self, req, resp, *args, **kwargs)
                    setattr(klass, responder_name, wrapper)
        if isinstance(uri_template, (list, tuple)):
            for template in uri_template:
                asgi.application.add_route(template, inst)
        else:
            asgi.application.add_route(uri_template, inst)
        return klass

    if isinstance(uri_template, (str, list, tuple)):
        return deco
    else:
        klass = uri_template
        uri_template = klass.uri_template
        return deco(klass)


def sink(prefix, *, security=None):
    def deco(sink):
        scopes = _get_default_security() if security is None else frozenset(security)
        if scopes:
            @functools.wraps(sink)
            async def wrapper(req, resp, **kwargs):
                await authorize(req, resp, scopes)
                await sink(req, resp, **kwargs)
        else:
            wrapper = sink
        asgi.application.add_sink(wrapper, prefix=prefix)

        return wrapper

    return deco


def _raise_401(auths=None):
    if auths is None:
        auths = Config.get_instance().authenticators
    challenges = []
    for auth in auths:
        challenge = auth.challenge()
        if challenge is not None:
            challenges.append(challenge)
    if challenges:
        raise HTTPUnauthorized(challenges=challenges)
    else:
        raise HTTPUnauthorized()


async def _check_scopes(req, outcome, scopes):
    req.context.user = outcome.user
    req.context.scopes = await outcome.get_scopes()
    if not scopes.issubset(req.context.scopes):
        if req.context.user is None:
            _raise_401()
        else:
            raise HTTPForbidden


async def authorize(req, resp, scopes):
    cfg = Config.get_instance()
    auths = cfg.authenticators
    try:
        for auth in auths:
            outcome = await auth.authenticate(req, resp)
            if outcome is not None:
                await _check_scopes(req, outcome, scopes)
                return
        else:
            await _check_scopes(req, AuthOutcome(), scopes)
    except AuthError:
        _raise_401(auths)


_MARKER = '_flowdas_authorized'


def _wrap_with_authorize(responder, scopes):
    @functools.wraps(responder)
    async def wrapper(self, req, resp, *args, **kwargs):
        await authorize(req, resp, scopes)
        await responder(self, req, resp, *args, **kwargs)

    setattr(wrapper, _MARKER, True)
    return wrapper


def security(*scopes):
    scopes = frozenset(scopes)

    def deco(responder):
        return _wrap_with_authorize(responder, scopes)

    return deco

