class System:
    def __init__(self, sysName: str, initHash: int, maxIntervalCount: int = 12, minimumObservedSpan: int = 6):
        # OBJECT PROPERTIES
        # unique identifier
        self.name = sysName
        # print(f"System {self.name} added to systemList")

        # universal across all Systems, consider moving to a higher scope (factory?) to save memory
        self.__maxIntvlCnt = maxIntervalCount
        self.__minSpan = minimumObservedSpan
        
        # OBJECT STATES
        self.isTicked = None
        # Tracked and Ticked: True
        # Tracked but not Ticked: False
        # Observed but not Tracked: None (System has sparse data)

        self.stateHashes = [None]*(maxIntervalCount-1)
        # ugh, should this have one for factionState monitoring and another for factionInfluence monitoring?

        self.stateHashes.append(initHash)
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0

    def performInterval(self):
        """Performs the system's status management - returns whether the system object should be deleted."""
        self.intrvlsSinceUpdate += 1

        # Move tracking window along and add empty slot for new data
        self.stateHashes.pop(0)
        self.stateHashes.append(None)

        # Delete the object if it has no data
        if self.intrvlsSinceUpdate >= self.__maxIntvlCnt:
            return True

        # Handle 'Ticked' Systems
        self.__updateIfTicked()
        self.__updateIfExpired()

        return False

    def __updateIfTicked(self):
        # Handle 'Ticked' Systems
        if self.isTicked == True:
            self.intrvlsSinceTick += 1
            if self.intrvlsSinceTick >= self.__maxIntvlCnt:
                # The point of this return is to ensure a ticked system remains tracked until the tick state goes out of scope
                
                self.isTicked = False
                self.intrvlsSinceTick = 0

    def __updateIfExpired(self):
        if self.isTicked == False:
            if self.intrvlsSinceUpdate >= self.__minSpan and self.isTicked == False:
                self.isTicked = None

    def receiveStateUpdate(self, hash: int):
        """Accepts a hash of a system's faction's overall state, handles whether that represents a new tick."""
        if self.intrvlsSinceUpdate > 0:
            if hash in self.stateHashes:
                self.__receiveStateUpdate(hash)
            else:
                self.__receiveStateChange(hash)
        
        # NB: This doesn't report a Tick on the System's first entry, because first entry occurs as part of the __init__

    def __receiveStateUpdate(self, hash: int):
        # State is already present in log (a normal Update), and current interval has not been updated
        self.stateHashes[(self.__maxIntvlCnt-1)] = hash
        self.intrvlsSinceUpdate = 0
        if self.isTicked == None:
            self.isTicked = False
        # print(f"System {self.name} received an update.")
    
    def __receiveStateChange(self, hash: int):
        # State is entirely new (a Tick has occurred)
        self.stateHashes[(self.__maxIntvlCnt-1)] = hash
        self.isTicked = True
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0
        print(f"System {self.name}'s faction influence has changed.")

systemList = []