async def receive_heartbeat_timeout(node: "Node"):
    from .node import NodeState
    # make it candidate and make it receive a bunch of votes
    node.state = NodeState.CANDIDATE
    for n in node.neighbors:
        node.countVotes[n] = False
    await node._post_neighbors("/start_election", {"nodeIP": node.IP})

async def receive_candidate_timeout(node: "Node"): ...

async def receive_heartbeat(node: "Node", data: object): ...

async def receive_vote(node: "Node", vote: bool): 
    print("We got a vote! Vote = %s", vote)

async def request_votes(node: "Node"): ...

async def receive_start_election(node: "Node", data: bool):
    print("hello world")