class NodeLog(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError("Key already exists")
        super().__setitem__(key, value)
