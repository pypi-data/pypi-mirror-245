import asyncio
import errno
import os
import signal

import falcon
import uvicorn

from flowdas.boot import Config
from flowdas.http import asgi, route
from flowdas.jsonrpc import Session

from .pidfile import Pidfile


class SessionImpl(Session):

    def __init__(self, root_class, ws, args):
        super().__init__(root_class)
        self._ws = ws
        self._sem = asyncio.Semaphore(Config.get_instance().max_session_rpc_concurrency)
        self._args = args

    @property
    def args(self):
        return self._args

    async def reader(self):
        while True:
            data = await self._ws.receive_text()
            await self._sem.acquire()
            try:
                asyncio.create_task(self._dispatch(data))
            except:
                self._sem.release()
                raise

    async def _dispatch(self, data):
        try:
            reply = await self._rpc.dispatch(self, data)
            if reply:
                await self._ws.send_text(reply)
        finally:
            self._sem.release()


class RpcResource:

    def __init__(self, root_class):
        self._root_class = root_class

    async def on_websocket(self, req, ws, *args):
        try:
            await ws.accept()
            session = SessionImpl(self._root_class, ws, args)
            await session.reader()
        except falcon.WebSocketDisconnected:
            return


class Server:
    _instance = None
    _ws_server = None
    _stop = None

    def run(self):
        Server._instance = self

        try:
            pidfile = Pidfile('f.pid')
            pidfile.create()
            try:
                cfg = Config.get_instance()
                # app = asgi.application
                for path in cfg.paths:
                    route(path.path)(RpcResource(path.root_class))
                    # app.add_route(path.path, RpcResource(path.root_class))
                uvicorn.run(asgi.application, host='0.0.0.0', port=9653)
            finally:
                pidfile.unlink()
        finally:
            Server._instance = None

    @classmethod
    def notify_shutdown(cls):
        pidfile = Pidfile('f.pid')
        pid = pidfile.validate()
        if pid:
            os.kill(pid, signal.SIGINT)
            print(pid)
            while True:
                try:
                    os.kill(pid, 0)
                except OSError as e:
                    if e.errno == errno.ESRCH:
                        break
