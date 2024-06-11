from uuid import uuid4

class Node:
    """
    Attributes:
        id (str): Unique identifier of the node. UUID4.
        neighbors (list[str]): List of neighbors of the node. 
    """
    def __init__(self, neighbors):
        self.uuid4 = uuid4()