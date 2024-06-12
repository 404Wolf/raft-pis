from uuid import uuid4
from queue import Queue
import socket
from enum import Enum
from .timer import NodeTimers
import logging

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

    async def _start(self):
        if self._task is None:
            self._task = asyncio.create_task(self._run())

    async def _run(self):
        while True:
            action = self.actionQueue.get()
            await action(self)
            _LOGGER.debug("Node action completed")

    async def add_action(self, action: coroutine):
        self.actionQueue.put(action)

    @staticmethod
    def _get_ip():
        return socket.gethostbyname(socket.gethostname())
