from time import time
from dataclasses import dataclass
from dataclasses import field
from .node import NodeState
from queue import Queue
import logging

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Term:
    """
    A term in the Raft.

    Attributes:
        number (int): The term number.
        timeStamp (int): The time the term was created.
    """

    number: int = 0
    timeStamp: int = field(default_factory=lambda: int(time()))

    def next_term(self) -> "Term":
        """
        Get the next term.
        """

        _LOGGER.debug("Next term", self.number + 1)
        return Term(self.number + 1)


@dataclass
class NodeLogEntry:
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

    def __init__(
        self, max_items: int, initial_state: NodeState, first_term: int = 0
    ) -> None:
        """
        Initialize the log with a cap on the number of items.
        """
        _LOGGER.debug("Initializing NodeLog")
        self.max_items = max_items
        self._log = [NodeLogEntry(None, Term(first_term), initial_state)]

    def append(self, data: object, state: NodeState) -> None:
        """
        Append a value to the log. Timestamp is automatically assigned.
        """
        self._log.append(NodeLogEntry(data, self.get().term.next_term(), state))
        _LOGGER.debug("Appended to log")

    def get(self) -> NodeLogEntry:
        """
        Get the most recent entry.
        """
        _LOGGER.debug("Getting most recent entry")
        return self._log[-1]
