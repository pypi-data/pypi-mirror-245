from datetime import datetime, date
import functools
import json

import falcon.asgi

__all__ = [
    'application',
    'add_app_hook',
]


async def error_handler(ex, req, resp, params):
    import traceback
    if isinstance(ex, (falcon.HTTPError, falcon.HTTPStatus)):
        if isinstance(ex, falcon.HTTPInternalServerError):
            traceback.print_exc()
    else:
        traceback.print_exc()
    raise


class DatetimeEncoder(json.JSONEncoder):
    """Json Encoder that supports datetime objects."""

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


json_handler = falcon.media.JSONHandler(
    dumps=functools.partial(json.dumps, cls=DatetimeEncoder),
)

_app_hooks = []


def add_app_hook(hook):
    hook(application)
    _app_hooks.append(hook)


def _create_application():
    app = falcon.asgi.App(cors_enable=True)
    app.add_error_handler(Exception, error_handler)

    extra_handlers = {
        'application/json': json_handler,
    }
    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)

    for hook in _app_hooks:
        try:
            hook(app)
        except:
            pass
    return app


application = _create_application()
