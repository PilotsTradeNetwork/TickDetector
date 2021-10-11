class System:
    def __init__(self, sysName: str, initHash: int, maxIntervalCount: int = 12, minFrequencyToTrack: int = 6):
        # OBJECT PROPERTIES
        # unique identifier
        self.name = sysName

        # universal across all Systems, consider moving to a higher scope (factory?) to save memory
        self.__maxIntvlCnt = maxIntervalCount
        self.__minSpan = minFrequencyToTrack
        
        # OBJECT STATES
        self.isTicked = None
        # Observed but not Tracked: None (System has sparse data)

        self.__hashes = [None]*(maxIntervalCount-1)
        # ugh, should this have one for factionState monitoring and another for factionInfluence monitoring?

        self.__hashes.append(initHash)
        self.__intrvlsSinceTick = 0
        self.__intrvlsSinceUpdate = 0

    def performInterval(self):
        """Performs the system's status management - returns whether the system object should be deleted."""
        self.__intrvlsSinceUpdate += 1

        # Move tracking window along and add empty slot for new data
        self.__hashes.pop(0)
        self.__hashes.append(None)

        if self.__intrvlsSinceUpdate >= self.__maxIntvlCnt:
            # System has no data, it will be deleted
            return False

        # Handle 'Ticked' Systems
        self.__iterateIfTicked()
        self.__iterateIfExpired()

        # Will be kept
        return True

    def receiveStateUpdate(self, hash: int):
        """Accepts a hash of a system's faction's overall state, handles whether that represents a new tick."""
        if self.__intrvlsSinceUpdate > 0:
            if hash in self.__hashes:
                self.__receiveStateUpdate(hash)
            else:
                self.__receiveStateChange(hash)
        else:
            return
        
        # NB: This doesn't report a Tick on the System's first entry, because first entry occurs as part of the __init__

    def __iterateIfTicked(self):
        # Handle 'Ticked' Systems
        if self.isTicked == True:
            self.__intrvlsSinceTick += 1
            if self.__intrvlsSinceTick >= self.__maxIntvlCnt:
                # The point of this return is to ensure a ticked system remains tracked until the tick state goes out of scope
                
                self.isTicked = False
                self.__intrvlsSinceTick = 0

    def __iterateIfExpired(self):
        if self.isTicked == False:
            if self.__intrvlsSinceUpdate >= self.__minSpan and self.isTicked == False:
                self.isTicked = None

    def __receiveStateUpdate(self, hash: int):
        # State is already present in log (a normal Update), and current interval has not been updated
        self.__hashes[(self.__maxIntvlCnt-1)] = hash
        self.__intrvlsSinceUpdate = 0
        if self.isTicked == None:
            self.isTicked = False
        # print(f"System {self.name} received an update.")
    
    def __receiveStateChange(self, hash: int):
        # State is entirely new (a Tick has occurred)
        self.__hashes[(self.__maxIntvlCnt-1)] = hash
        self.isTicked = True
        self.__intrvlsSinceTick = 0
        self.__intrvlsSinceUpdate = 0
        print(f"System {self.name}'s faction influence has changed.")

systemList = []