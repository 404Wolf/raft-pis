class NodeLog(dict):
    """"
    """

    def __init__(self, start, max_items: int):
        self.max_items = max_items
        super().__init__(start)

    def __setitem__(self, key, value):
        # If the 
