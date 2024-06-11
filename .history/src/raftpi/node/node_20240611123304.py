from uuid import uuid4
from enum import Enum

class NodeState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class Node:
    """
    Attributes:
        id (UUID): Unique identifier of the node. UUID4.
        neighbors (list[UUID]): List of neighbors of the node. 

    """
    def __init__(self, neighbors: list[str]):
        self.uuid4 = uuid4()
        self.neighbors = neighbors