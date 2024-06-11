class NodeLog:
    """
    A log with timestamps and values for a Raft node, with a cap on the number of items.
    Each node has its own NodeLog.
    """

    def __init__(self, start, max_items: int):
        self.max_items = max_items
        super().__init__(start)

    def append(self, value):
        ...

    def get(self):
        """
        Get the most recent entry
        """