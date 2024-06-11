from uuid import uuid4
from queue import Queue
import socket
from enum import Enum


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

    async def run(self):
        while True:
            action = self.actionQueue.get()
            await action(self)

    @staticmethod
    def _get_ip():
        return socket.gethostbyname(socket.gethostname())
