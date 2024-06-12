import aiohttp
from queue import Queue
from .api import API
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
from ..config import DEFAULT_TIMER
from raftpi.node import actions

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
        self.countVotes = dict()
        self.timers = NodeTimers(
            DEFAULT_TIMER,
            DEFAULT_TIMER,
            actions.receive_candidate_timeout(self),
            actions.receive_heartbeat_timeout(self),
        )
        self._start_task = None

    def _setup_api(self):
        """Setup the API with the receivers and sender utilities."""
        self.api = API(
            receive_vote_callback=self._receive_vote_handler,
            receive_start_election_callback=self._receive_start_election_handler,
            receive_heartbeat_callback=self._receive_heartbeat_handler,
            receive_append_callback=self._receive_append_handler,
        )
        self.api.run()

    async def start(self):
        """Start the node processes."""
        if self._start_task is None:
            self._setup_api()

            # start the heartbeat timer and push the heartbeat timeout to the actions queue
            if self.state == NodeState.FOLLOWER:
                asyncio.create_task(self.timers.start_heartbeat_timer())

            self._start_task = asyncio.create_task(self._begin_actions())

    async def _begin_actions(self):
        """Start the node actions."""
        print("starting action queue runner")
        while True:
            print("Checking queue")
            action = self.actionQueue.get()
            print(action)
            asyncio.create_task(action())
            await asyncio.sleep(.3)
            print("Awaited the sleep")
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

    async def _receive_vote_handler(self, vote: bool):
        """Receive a vote from a requesting node."""
        async def _wrapped_receive_vote():
            await actions.receive_vote(self, vote)
        self.add_action(_wrapped_receive_vote)
    
    async def _receive_start_election_handler(self, data: bool):
        self.add_actions(actions.receive_start_election(data))

    async def _send_vote(self, vote: bool):
        """Send a vote to the requesting node."""
        if self.state == NodeState.FOLLOWER:
            await self._post_neighbors("vote", {"vote": vote})
        else:
            raise Node.WrongStateException("Node is not a follower")

    async def _receive_heartbeat_handler(self, data: dict):
        pass

    async def _send_heartbeat(self):
        """Send a heartbeat to the requesting node."""
        if self.state == NodeState.LEADER:
            await self._post_neighbors("heartbeat")
        else:
            raise Node.WrongStateException("Node is not a leader")

    async def _receive_append_handler(self, data: object):
        pass

    async def _send_append(self):
        """Send an append to the requesting node."""
        await self._post_neighbors("append")

    def add_action(self, action: Coroutine):
        """Add an action to the action queue."""
        self.actionQueue.put(action)
        _LOGGER.debug("Node action completed")

    @staticmethod
    def _get_ip() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                                                                                                                                
        s.settimeout(0)                                                                                                                                                                                                     
        try:                                                                                                                                                                                                                
            s.connect(('8.8.8.8', 1))  # Google's DNS server                                                                                                                                                                
            ip_address = s.getsockname()[0]                                                                                                                                                                                 
        except Exception:                                                                                                                                                                                                   
            ip_address = '127.0.0.1'  # Localhost as fallback                                                                                                                                                               
        finally:                                                                                                                                                                                                            
            s.close()
        print(ip_address)
        return ip_address
        # IP = socket.gethostbyname(socket.gethostname())
        # _LOGGER.info(f"Node IP: {IP}")
        # return IP

