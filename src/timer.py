import asyncio
from time import time


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self.run = False
        self._time = None
        self._task = None

    def start(self) -> None:
        if self.run:
            return

        self._time = time()
        self.run = True
        self._task = asyncio.ensure_future(self._loop())

    def stop(self) -> None:
        self.run = False

    def reset(self) -> None:
        if self.run:
            self._time = time()

    async def _loop(self) -> None:
        while (time() - self._time) < self._timeout and self.run:
            await asyncio.sleep(0.2)

        await self._callback()
        self.run = False
