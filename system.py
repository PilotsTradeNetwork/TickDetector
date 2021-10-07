

from zmq.backend import has


class System:
    def __init__(self, sysName: str, initHash: int, maxIntervalCount: int = 12, minimumObservedSpan: int = 6):
        # OBJECT PROPERTIES

        # unique identifier
        self.name = sysName

        # universal across all Systems, consider moving to a higher scope (factory?) to save memory
        self.__maxIntvlCnt = maxIntervalCount
        self.__minSpan = minimumObservedSpan
        
        # OBJECT STATES
        self.isTicked = None
        # Tracked and Ticked: True
        # Track and not ticked: False
        # Observed but not tracked: None (Systems has sparse data)

        self.stateHashes = [None]*11
        # ugh, should this have one for factionState monitoring and another for factionInfluence monitoring?

        self.stateHashes.append(initHash)
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0

    def performInterval(self):
        """Performs the system's status management - returns whether the system object should be deleted."""
        self.intrvlsSinceUpdate += 1

        # Move tracking window along and add empty slot for new data
        self.stateHashes = self.stateHashes[1:(self.__maxIntvlCnt-1)]
        self.stateHashes.append(None)

        # Delete the object if it has no data
        if self.isTicked == None and self.intrvlsSinceUpdate >= self.__maxIntvlCnt:
            return True

        # Handle 'Ticked' Systems
        if not self.__updateIfTicked():
            # Handle unticked Systems
            self.__updateIfExpired()

        return False

    def __updateIfTicked(self):
        # Handle 'Ticked' Systems
        if self.isTicked == True:
            self.intrvlsSinceTick += 1

            if self.intrvlsSinceTick < self.__maxIntvlCnt:
                # The point of this return is to preserve ticked system in the observation window until the tick goes out of scope
                return True
            self.isTicked = False
            self.intrvlsSinceTick = 0
        return False

    def __updateIfExpired(self):
        if self.intrvlsSinceUpdate >= self.__minSpan:
            self.isTicked = None

    def receiveStateUpdate(self, hash: int):
        """Accepts a hash of a system's faction's overall state, handles whether that represents a new tick."""
        if not self.__receiveStateUpdate(hash):
            self.__receiveStateChange(hash)
        
        # NB: This doesn't report a Tick on the System's first entry, because first entry occurs as part of the __init__

    def __receiveStateUpdate(self, hash: int):
        # State is already present in log (a normal Update), and current interval has not been updated
        if self.intrvlsSinceUpdate > 0 and hash in self.stateHashes:
            self.stateHashes[(self.__maxIntvlCnt-1)] = hash
            self.intrvlsSinceUpdate = 0
            return True
        return False
    
    def __receiveStateChange(self, hash: int):
        # State is entirely new (a Tick has occurred)
        self.stateHashes[(self.__maxIntvlCnt-1)] = hash
        self.isTicked = True
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0