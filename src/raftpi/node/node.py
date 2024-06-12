from uuid import uuid4
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

    def __init__(self, neighbors: list[str]):
        self.IP = self._get_ip()
        self.neighbors = neighbors
        self.actionQueue = Queue()
        self.timers = NodeTimers()
        self._start_task = None

    async def start(self):
        """Start the node processes."""

        if self._start_task is None:
            self._start_task = asyncio.create_task(self._begin_actions())

    async def _begin_actions(self):
        while True:
            await (await self.actionQueue.get())(self)
            await asyncio.sleep(3)

    @app.route("/vote")
    async def _receive_vote(self, request: Request): ...

    async def _send_vote(self):
        """Send a vote to the requesting node."""
        pass

    @app.route("/heartbeat")
    async def _receive_heartbeat(self, request: Request): ...

    async def _send_heartbeat(self):
        """Send a heartbeat to the requesting node."""
        pass

    @app.route("/append")
    async def _receive_append(self, request: Request): ...

    async def _send_append(self):
        """Send an append to the requesting node."""
        pass

    async def add_action(self, action: Coroutine):
        """Add an action to the action queue."""
        self.actionQueue.put(action)
        _LOGGER.debug("Node action completed")

    @staticmethod
    def _get_ip():
        IP = socket.gethostbyname(socket.gethostname())
        _LOGGER.info(f"Node IP: {IP}")
        return IP


uvicorn.run(app, host="localhost", port=8000)
