import asyncio
import concurrent.futures
import functools
import inspect
import os

import nest_asyncio

__all__ = [
    'await_sync',
    'function',
    'resolve',
]

_executor = None
_in_executor = False


def _init_executor():
    # executor 에서 실행 중임을 알려준다.
    global _in_executor
    _in_executor = True
    # executor process 의 우선 순위를 낮춘다.
    os.nice(20)
    # uvloop 와 nest_asyncio 의 충돌을 피하기위해 policy 를 초기화한다.
    asyncio.set_event_loop_policy(None)
    # fork 한 상황에서 parent 의 event loop 를 지우고 새로 만든다.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # run_until_complete 의 중첩을 허락한다
    nest_asyncio.apply()


def _call_sync_impl(wrapper, ba):
    # pickle 하기 위해서 전역 함수 사용
    return wrapper.__wrapped__(*ba.args, **ba.kwargs)


_functions = {}


def function(_=None, *, name: str = None):
    def deco(impl):
        if name is None:
            mods = []
            for mod in reversed(impl.__module__.split('.')):
                if mod.startswith('_'):
                    break
                mods.append(mod)
            mods.reverse()
            mods.append(impl.__qualname__)
            key = '.'.join(mods)
        else:
            key = name
        if key in _functions:
            raise KeyError

        if asyncio.iscoroutinefunction(impl) or inspect.isasyncgenfunction(impl):
            _functions[key] = impl
            return impl
        elif inspect.isgeneratorfunction(impl):
            raise TypeError(
                'synchronous generator not supported. use async generator.')
        elif callable(impl):
            sig = inspect.signature(impl)

            # TypeError 를 일찍 발생시키기 위해 future 를 반환하는 동기 함수로 제작한다.
            @functools.wraps(impl)
            def wrapper(*args, **kwargs):
                global _executor

                if _in_executor:
                    # 이미 Executor 에서 실행 중이면 직접 실행한다.
                    result = impl(*args, **kwargs)

                    async def _return():
                        return result
                    return _return()

                loop = asyncio.get_event_loop()
                if _executor is None:
                    _executor = concurrent.futures.ProcessPoolExecutor(
                        initializer=_init_executor)

                # 전달된 인자가 함수의 서명과 호환되지 않으면 일찍 TypeError 를 발생시킨다.
                ba = sig.bind(*args, **kwargs)

                # impl 을 전달하면 unpickle 될 때 impl 의 fqdn 에는 wrapper 가 있어서 에러가 발생한다.
                # 따라서 wrapper 를 전달하고 wrapper.__wrapped__ 를 호출한다.
                return loop.run_in_executor(_executor, _call_sync_impl, wrapper, ba)

            _functions[key] = wrapper
            return wrapper
        else:
            raise TypeError(f'not supprrted type: {type(impl)}')

    if _ is None:
        return deco
    else:
        return deco(_)


def await_sync(awaitable):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(awaitable)


def resolve(name):
    return _functions.get(name)
