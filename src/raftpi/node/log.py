from time import time
from dataclasses import dataclass
from .node import NodeState
from queue import Queue


class Term:
    lastTerm = 0

    def __init__(self) -> None:
        self.lastTerm = Term.lastTerm
        self.timeStamp = time()
        Term.lastTerm += 1


@dataclass
class NodeData:
    """
    Data for a Raft node.
    """

    data: object
    term: Term
    state: NodeState


class NodeLog:
    """
    A log with timestamps and values for a Raft node, with a cap on the number of items.
    Each node has its own NodeLog.
    """

    def __init__(self, max_items: int) -> None:
        """
        Initialize the log with a cap on the number of items.
        """
        self.max_items = max_items
        self.log = []

    def current_term(self) -> Term:
        """Get the current term."""
        if len(self.log) == 0:
            return Term()
        return self.log[-1]

    def append(self, data, state) -> None:
        """
        Append a value to the log. Timestamp is automatically assigned.
        """
        self.log.append(NodeData(data, Term(), state))

    def get(self) -> NodeData:
        """
        Get the most recent entry.
        """
        return self.log[-1]
