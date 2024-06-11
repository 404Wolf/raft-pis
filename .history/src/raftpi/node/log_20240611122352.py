class NodeLog(dict):
    """
    A log of all the entries that have been appended to the log.
    """

    def __init__(self, start, max_items: int):
        self.max_items = max_items
        super().__init__(start)

    def __setitem__(self, key, value):
        # If the 
