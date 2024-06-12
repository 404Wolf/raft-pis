import aiohttp
from queue import Queue
from fastapi import Request
import contextlib
import threading
import socket
from enum import Enum
import time
from .timer import NodeTimers
import asyncio
from typing import Coroutine
from fastapi import FastAPI
import logging
import uvicorn
from threading import Thread

app = FastAPI()

_LOGGER = logging.getLogger(__name__)


class NodeState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3


class Node:
    """
    Attributes:
        IP (str): IP address of the node.
        neighbors (list[UUID]): List of neighbors of the node.
        log: (NodeLog): Log of the node.
        state (NodeState): Current state of the node.
    """

    class WrongStateException(Exception):
        """Raised when the node is in the wrong state for the action."""

        pass

    def __init__(self, neighbors: list[str], state: NodeState = NodeState.FOLLOWER):
        self.IP = self._get_ip()
        self.state = state
        self.neighbors = neighbors
        self.actionQueue = Queue()
        self.timers = NodeTimers()
        self._start_task = None

    async def start(self):
        """Start the node processes."""

        if self._start_task is None:
            self._start_task = asyncio.create_task(self._begin_actions())

    async def _begin_actions(self):
        """Start the node actions."""
        while True:
            await (await self.actionQueue.get())(self)
            await asyncio.sleep(3)
            _LOGGER.debug("Node action completed")

    async def _post_neighbors(self, endpoint: str, data: dict = {}):
        """Send a request to all neighbors."""
        async with aiohttp.ClientSession() as session:
            for neighbor in self.neighbors:
                async with session.post(
                    f"http://{neighbor}/{endpoint}", json=data
                ) as response:
                    response = await response.json()
                    _LOGGER.debug(response)

    @app.route("/vote", methods=["POST"])
    async def _receive_vote(self, request: Request):
        """Receive a vote from a requesting node."""
        pass

    async def _send_vote(self, vote: bool):
        """Send a vote to the requesting node."""
        if self.state == NodeState.FOLLOWER:
            await self._post_neighbors("vote", {"vote": vote})
        else:
            raise Node.WrongStateException("Node is not a follower")

    @app.route("/heartbeat", methods=["POST"])
    async def _receive_heartbeat(self, request: Request): ...

    async def _send_heartbeat(self):
        """Send a heartbeat to the requesting node."""
        if self.state == NodeState.LEADER:
            await self._post_neighbors("heartbeat")
        else:
            raise Node.WrongStateException("Node is not a leader")

    @app.route("/append", methods=["POST"])
    async def _receive_append(self, request: Request):
        pass

    async def _send_append(self):
        """Send an append to the requesting node."""
        await self._post_neighbors("append")

    async def add_action(self, action: Coroutine):
        """Add an action to the action queue."""
        self.actionQueue.put(action)
        _LOGGER.debug("Node action completed")

    @staticmethod
    def _get_ip():
        IP = socket.gethostbyname(socket.gethostname())
        _LOGGER.info(f"Node IP: {IP}")
        return IP


Thread(target=lambda: uvicorn.run(app, host="localhost", port=8000)).start()
