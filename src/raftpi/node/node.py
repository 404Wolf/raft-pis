from uuid import uuid4
from queue import Queue
import socket
from enum import Enum


class NodeState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3


class NodeTimers:
    """
    Attributes:
        election_timer (int): Time in milliseconds for the election timer.
        heartbeat_timer (int): Time in milliseconds for the heartbeat timer.
    """

    def __init__(self, election_timer: int = 0, heartbeat_timer: int = 0):
        self.election_timer = election_timer
        self.heartbeat_timer = heartbeat_timer

    async def reset_election_timer(self): ...

    async def reset_heartbeat_timer(self): ...

    async def start_election_timer(self): ...

    async def start_heartbeat_timer(self): ...


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

    async def run(self):
        while True:
            action = self.actionQueue.get()
            await action()

    @staticmethod
    def _get_ip():
        return socket.gethostbyname(socket.gethostname())
