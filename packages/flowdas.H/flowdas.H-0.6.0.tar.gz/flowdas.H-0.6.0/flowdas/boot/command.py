import asyncio
import getopt
import inspect
import re
import sys
import traceback

from typeable import cast, Context

PARAM_REGEX = re.compile(r'^\s*:param\s+(?P<type>\w+\s+)?(?P<name>\w+):\s*(?P<doc>.*)$', re.MULTILINE)

_cmdmap = {}


def command(_=None, *, namespace: str = None):
    def deco(func):
        if namespace:
            name = f'{namespace}.{func.__name__}'
        else:
            name = func.__name__
        _cmdmap[name] = func

    if _ is None:
        return deco
    else:
        return deco(_)


def parse_doc(doc):
    # returns (synopsis, {name: doc})

    lines = (doc or '').strip().split('\n')
    if len(lines) == 1:
        return lines[0].strip(), {}
    elif len(lines) >= 2 and not lines[1].rstrip():
        synopsis = lines[0].strip()
        desc = '\n'.join(lines[2:])
    else:
        synopsis = ''
        desc = '\n'.join(lines)

    return synopsis, dict((name.strip(), doc.strip()) for _, name, doc in PARAM_REGEX.findall(desc))


def usage(command: str = None):
    if command and command in _cmdmap:
        func = _cmdmap[command]
        print(f'{command}{inspect.signature(func)}')
        synopsis, params = parse_doc(func.__doc__)
        print(synopsis)
        print()
        for param, desc in params.items():
            print(f'{param}\t{desc}')
    else:
        for name, func in sorted(_cmdmap.items()):
            print(f'{name}{inspect.signature(func)}')
            synopsis, _ = parse_doc(func.__doc__)
            if synopsis:
                print(f'    {synopsis}')


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # parse options
    try:
        opts, args = getopt.getopt(argv[1:], 'hv')
    except getopt.GetoptError as e:
        print(e)
        usage()
        sys.exit(2)
    verbose = False
    for o, _ in opts:
        if o == '-h':
            usage(args[0] if args else None)
            sys.exit()
        elif o == '-v':
            verbose = True
        else:
            assert False, "unknown option"

    # resolve command
    if not args:
        usage()
        sys.exit()

    try:
        func = _cmdmap[args[0]]
    except KeyError:
        print(f"Error: No such command '{args[0]}'.")
        usage()
        sys.exit(2)

    f_args = []
    f_kwargs = {}
    for arg in args[1:]:
        fields = arg.split('=', 1)
        if len(fields) > 1:
            f_kwargs[fields[0]] = fields[1]
        else:
            f_args.append(arg)

    f = cast.function(func)
    ctx = Context()
    try:
        with ctx.capture() as error:
            result = f(*f_args, **f_kwargs, ctx=ctx)
            if inspect.iscoroutinefunction(func):
                result = asyncio.get_event_loop().run_until_complete(result)
        if result is not None:
            print(result)
    except Exception as e:
        if isinstance(e, TypeError):
            print(f'Error at {error.location}::{e}')
        elif verbose:
            traceback.print_exc()
        else:
            print(e)
        sys.exit(2)
