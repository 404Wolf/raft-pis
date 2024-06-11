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
        self.log = dict()

    def append(self, value):
        """
        Append a value to the log. Timestamp is automatically assigned.
        """

    def get(self):
        """
        Get the most recent entry.
        """