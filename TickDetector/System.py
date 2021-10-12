class System:
    def __init__(self, sysName: str, initHash: int, maxIntervalCount: int = 12):
        # unique identifier
        self.name = sysName
        
        # OBJECT STATES
        self.isTicked = None
        # Observed but not Tracked: None (System has sparse data)

        self.hashes = [None]*(maxIntervalCount-1)
        # ugh, should this have one for factionState monitoring and another for factionInfluence monitoring?

        self.hashes.append(initHash)
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0
