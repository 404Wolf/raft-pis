import logging

import uvicorn
from threading import Thread
import aiohttp
import asyncio
from fastapi import FastAPI, Request, APIRouter
from pydantic import BaseModel

_LOGGER = logging.getLogger(__name__)
class VoteBool(BaseModel):
    vote: bool


class API:
    def __init__(
        self,
        receive_vote_callback,
        receive_start_election_callback,
        receive_heartbeat_callback,
        receive_append_callback,
    ):
        self.receive_vote_callback = receive_vote_callback
        self.receive_start_election_callback = receive_start_election_callback
        self.receive_heartbeat_callback = receive_heartbeat_callback
        self.receive_append_callback = receive_append_callback
        self.app = FastAPI()
        self._router()

    def _router(self):
        self.router = APIRouter()
        self.router.add_api_route("/vote", self._receive_vote, methods=["POST"])
        self.app.include_router(self.router)

    async def _receive_vote(self, vote_bool: VoteBool):
        """Receive a vote from a requesting node."""
        await self.receive_vote_callback(vote_bool.vote)

    def run(self):
        """Run the API."""
        _LOGGER.debug("Running API")
        Thread(target=lambda: uvicorn.run(self.app, host="localhost", port=8000)).start()

    async def send(self, ip: str, endpoint: str, data: object, port: int = 8000):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{ip}:{port}/{endpoint}", json=data
            ) as response:
                response = await response.json()
                _LOGGER.debug(response)
    
    # @app.post("/start_election/")
    # @staticmethod
    # async def _receive_start_election(vote_bool: VoteBool):
        # """A node sends its vote over."""
        # await API.receive_start_election_callback(vote_bool.vote)


    async def _send_vote(self, ip: str, vote: bool):
        """Send a vote to the requesting node."""
        await self.send(ip, "vote", data={"vote": vote})

    # @app.route("/heartbeat", methods=["POST"])
    # @staticmethod
    # async def _receive_heartbeat(request: Request):
    #     """Receive a heartbeat from a requesting node."""
    #     await API.receive_heartbeat_callback()

    async def _send_heartbeat(self, ip: str):
        """Send a heartbeat to the requesting node."""
        await self.send(ip, "heartbeat", data={})

    # @app.route("/append", methods=["POST"])
    # @staticmethod
    # async def _receive_append(request: Request):
    #     """Receive an append from a requesting node."""
    #     await API.receive_append_callback((await request.json()).data)

    async def _send_append(self, ip: str, data: object):
        await self.send(ip, "append", data=data)
