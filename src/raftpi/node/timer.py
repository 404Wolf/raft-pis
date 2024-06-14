import asyncio
from typing import Awaitable
import logging

_LOGGER = logging.getLogger(__name__)


class NodeTimer:
    def __init__(self, duration: int, callback: Awaitable | None = None):
        self.duration = duration
        if callback:
            self._callback = callback
        self._task = None

    async def _run(self):
        print("timer is running")
        await asyncio.sleep(3)
        print("done timer")
        if self._callback:
            await self._callback()
            print("running callback!")
            _LOGGER.debug("Ran the callback")
        else:
            _LOGGER.debug("No callback provided")
        _LOGGER.debug("Timer expired")

    async def start(self):
        """
        Start the timer.
        """
        # await the start 
        await self._run()


        # print("starting a timer")
        # self._task = asyncio.create_task(self._run())
        # await self._run()

    async def reset(self):
        """
        Reset the timer.
        """
        if self._task:
            self._task.cancel()
        await self.start()

    async def stop(self):
        """
        Stop the timer.
        """
        if self._task:
            self._task.cancel()
            self._task = None


class NodeTimers:
    """
    Attributes:
        election_timer (int): Time in milliseconds for the election timer.
        heartbeat_timer (int): Time in milliseconds for the heartbeat timer.
    """

    def __init__(
        self,
        election_timer: int = 0,
        heartbeat_timer: int = 0,
        election_callback: Awaitable | None = None,
        heartbeat_callback: Awaitable | None = None,
    ):
        self.election_timer = NodeTimer(election_timer, election_callback)
        self.heartbeat_timer = NodeTimer(heartbeat_timer, heartbeat_callback)

    async def reset_election_timer(self):
        await self.election_timer.reset()

    async def reset_heartbeat_timer(self):
        await self.heartbeat_timer.reset()

    async def start_election_timer(self):
        await self.election_timer.start()

    async def start_heartbeat_timer(self):
        print("starting heartbeat timer")
        self._task = asyncio.create_task(self.heartbeat_timer.start())
        # await asyncio.sleep(.1)
