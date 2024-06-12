from node import NodeState

async def receive_heartbeat_timeout(self):
    # make it candidate and make it receive a bunch of votes
    self.state = NodeState.CANDIDATE
    # await self._send_vote()

    pass
async def receive_candidate_timeout(): ...


async def receive_heartbeat(data: object): ...


async def receive_vote(vote: bool): ...


async def request_votes(): ...
