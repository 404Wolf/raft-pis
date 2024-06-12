import logging

import uvicorn
from threading import Thread
import aiohttp
import asyncio
from fastapi import FastAPI, Request

from .node import Node, NodeState

_LOGGER = logging.getLogger(__name__)
app = FastAPI()


class API:
    def __init__(
        self,
        receive_vote_callback,
        receive_heartbeat_callback,
        receive_append_callback,
    ):
        self.receive_vote_callback = receive_vote_callback
        self.receive_heartbeat_callback = receive_heartbeat_callback
        self.receive_append_callback = receive_append_callback

    def run(self):
        """Run the API."""
        Thread(target=lambda: uvicorn.run(app, host="localhost", port=8000)).start()

    async def send(self, ip: str, endpoint: str, data: object, port: int = 8000):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{ip}:{port}/{endpoint}", json=data
            ) as response:
                response = await response.json()
                _LOGGER.debug(response)

    @app.route("/vote", methods=["POST"])
    async def _receive_vote(self, request: Request):
        """Receive a vote from a requesting node."""
        await self.receive_vote_callback((await request.json()).vote)

    async def _send_vote(self, ip: str, vote: bool):
        """Send a vote to the requesting node."""
        await self.send(ip, "vote", data={"vote": vote})

    @app.route("/heartbeat", methods=["POST"])
    async def _receive_heartbeat(self, request: Request):
        """Receive a heartbeat from a requesting node."""
        await self.receive_heartbeat_callback()

    async def _send_heartbeat(self, ip: str):
        """Send a heartbeat to the requesting node."""
        await self.send(ip, "heartbeat", data={})

    @app.route("/append", methods=["POST"])
    async def _receive_append(self, request: Request):
        """Receive an append from a requesting node."""
        await self.receive_append_callback((await request.json()).data)

    async def _send_append(self, ip: str, data: object):
        await self.send(ip, "append", data=data)
