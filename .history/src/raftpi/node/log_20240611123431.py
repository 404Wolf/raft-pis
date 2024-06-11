from time import time
from dataclasses import dataclass
from .node import NodeState

@dataclass
class NodeData:
    """
    Data for a Raft node.
    """
    value: object
    state: NodeState

class NodeLog:
    """
    A log with timestamps and values for a Raft node, with a cap on the number of items.
    Each node has its own NodeLog.
    """
    
    def __init__(self, max_items: int):
        """
        Initialize the log with a cap on the number of items.
        """
        self.max_items = max_items
        self.log = []

    def _get_timestamp(self):
        """
        Get the current timestamp.
        """
        return time()

    def append(self, value):
        """
        Append a value to the log. Timestamp is automatically assigned.
        """
        self.log[self._timestamp()] = value

    def get(self):
        """
        Get the most recent entry.
        """