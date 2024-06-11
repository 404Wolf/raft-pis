class NodeLog:
    """
    A log with timestamps and values for a Raft node.
    """

    def __init__(self, start, max_items: int):
        self.max_items = max_items
        super().__init__(start)

    def __setitem__(self, key, value):
        # If the 
