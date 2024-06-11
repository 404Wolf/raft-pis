class NodeTimer:
    def __init__(self, duration: int):
        self.duration = duration

    async def start(self): 
        """
        Start the timer.
        """
    
    async def reset(self):
        """
        Reset the timer.
        """

    async def stop(self):
        """
        Stop the timer.
        """

class NodeTimers:
    """
    Attributes:
        election_timer (int): Time in milliseconds for the election timer.
        heartbeat_timer (int): Time in milliseconds for the heartbeat timer.
    """

    def __init__(self, election_timer: int = 0, heartbeat_timer: int = 0):
        self.election_timer = election_timer
        self.heartbeat_timer = heartbeat_timer

    async def reset_election_timer(self): ...

    async def reset_heartbeat_timer(self): ...

    async def start_election_timer(self): ...

    async def start_heartbeat_timer(self): ...

