from flowdas.boot import command, define
from typeable import field

from .auth import (
    Authenticator,
    ApiKeyAuthenticator,
    ApiKeyService,
    ApiKeyConfigService,
    UserService,
    UserConfigService,
)

#
# configuration
#

define('anonymous', frozenset[str], field(default_factory=frozenset))
define('apikey', ApiKeyService, ApiKeyConfigService())
define('authenticators', list[Authenticator], field(default_factory=lambda: [ApiKeyAuthenticator()]))
define('security', frozenset[str], field(default_factory=frozenset))
define('user', UserService, UserConfigService())


#
# commands
#

@command()
def http(method: str, path: str, *args: str, measure: bool = False, profile: bool = False, **kwargs):
    import cProfile
    import timeit
    import traceback
    import falcon.testing
    from .asgi import application

    if profile:
        measure = True

    method = method.upper()

    headers = {}
    params = kwargs
    body = []
    if 'body' in kwargs:
        b = kwargs.pop('body')
        if isinstance(b, list):
            body.extend(b)
        else:
            body.append(b)

    def add_param(key, value):
        if key == 'body':
            body.append(value or '')
        else:
            if key in params:
                params[key].append(val)
            else:
                params[key] = [val]

    for arg in args:
        n = len(arg)
        idx = min(arg.find(':') % (n + 1), arg.find('=') % (n + 1))
        if idx == n:
            key = arg.strip()
            add_param(key, None)
        else:
            sep = arg[idx]
            key = arg[:idx].strip()
            val = arg[idx + 1:].strip()
            if sep == '=':
                add_param(key, val)
            else:
                headers[key] = val
    opts = {}
    if params:
        opts['params'] = params
    if headers:
        opts['headers'] = headers
    if body:
        opts['body'] = ''.join(body)

    if measure:
        client = falcon.testing.TestClient(application)

        def run():
            client.simulate_request(method, path, **opts)

        stmt = 'run()'
        t = timeit.Timer(stmt, globals={'run': run})
        try:
            number, _ = t.autorange()
        except:
            t.print_exc()
            return

        if profile:
            raw_timings = None

            def prun():
                nonlocal raw_timings
                raw_timings = t.repeat(number=number)

            try:
                cProfile.runctx('prun()', globals={'prun': prun}, locals={}, sort='cumulative')
            except:
                traceback.print_exc()
                return
        else:
            try:
                raw_timings = t.repeat(number=number)
            except:
                t.print_exc()
                return
        timings = [dt / number for dt in raw_timings]

        units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
        precision = 3

        def format_time(dt):
            unit = None

            scales = [(scale, unit) for unit, scale in units.items()]
            scales.sort(reverse=True)
            for scale, unit in scales:
                if dt >= scale:
                    break

            return "%.*g %s" % (precision, dt / scale, unit)

        best = min(timings)
        print("%d loop%s, best of %d: %s per loop"
              % (number, 's' if number != 1 else '',
                 len(timings), format_time(best)))

        best = min(timings)
        worst = max(timings)
        if worst >= best * 4:
            import warnings
            warnings.warn_explicit("The test results are likely unreliable. "
                                   "The worst time (%s) was more than four times "
                                   "slower than the best time (%s)."
                                   % (format_time(worst), format_time(best)),
                                   UserWarning, '', 0)

    else:
        client = falcon.testing.TestClient(application)
        r = client.simulate_request(method, path, **opts)
        print('HTTP/1.1 %s' % r.status)
        for name in r.headers:
            print('%s: %s' % (name, r.headers[name]))
        print('')
        if r.content:
            print(r.content)
