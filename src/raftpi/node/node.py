from uuid import uuid4
from queue import Queue
import socket
from enum import Enum
from .timer import NodeTimers
import asyncio
from typing import Coroutine
from fastapi import FastAPI

app = FastAPI()

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

    @app.route("/")
    async def _run_flask():
        return "Hello, World!"

    async def _start(self):
        """Start the node processes."""
        

        if self._start_task is None:
            self._start_task = asyncio.create_task(self._run())

    async def _run(self):
        while True:
            await (await self.actionQueue.get())(self)
            await asyncio.sleep(3)

    async def add_action(self, action: Coroutine):
        self.actionQueue.put(action)

    @staticmethod
    def _get_ip():
        return socket.gethostbyname(socket.gethostname())
