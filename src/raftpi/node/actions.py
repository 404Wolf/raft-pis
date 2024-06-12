from node import NodeState, Node

async def receive_heartbeat_timeout(node: Node):
    # make it candidate and make it receive a bunch of votes
    node.state = NodeState.CANDIDATE
    # await self._send_vote()

async def receive_candidate_timeout(node: Node): ...


async def receive_heartbeat(node: Node, data: object): ...


async def receive_vote(node: Node, vote: bool): ...


async def request_votes(node: Node): ...
