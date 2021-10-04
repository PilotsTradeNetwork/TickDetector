

class System:
    def __init__(self, sysName: str, initHash: int, maxIntervalCount: int = 12, minimumObservedSpan: int = 6):
        # OBJECT PROPERTIES

        # unique identifier
        self._name = sysName

        # universal across all Systems, consider moving to a higher scope (factory?) to save memory
        self.__maxIntvlCnt = maxIntervalCount
        self.__minSpan = minimumObservedSpan
        
        # OBJECT STATES
        self.isTicked = None
        # Tracked and Ticked: True
        # Track and not ticked: False
        # Observed but not tracked: None (Systems has sparse data)
        self.stateHashes = [None]*11
        self.stateHashes.append(initHash)
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0

        self.deletionMark = False

    # Called every 5 minutes
    def performInterval(self):
        """Performs the system's status management, designed to work on 5 minute intervals."""
        self.intrvlsSinceUpdate += 1

        # Move tracking window along
        self.stateHashes = self.stateHashes[1:(self.__maxIntvlCnt-1)]

        # Add empty slot for new data
        self.stateHashes.append(None)
        
        # Delete and stop tracking the object if it has no data
        if self.intrvlsSinceUpdate >= self.__maxIntvlCnt:
            self.deletionMark = True
            self.isTicked = None
            return

        # Logic to update 'Ticked' systems
        if self.isTicked == True:
            self.intrvlsSinceTick += 1

            # System's tick has exited observation window, mark as false and subject to screening
            if self.intrvlsSinceTick > self.__maxIntvlCnt:
                self.isTicked = False
                self.intrvlsSinceTick = 0
            # System ticked within observation window, maintain it
            else:
                return
        
        # Screening
        # Stop tracking ticked state if only 1 observation exists in the pool
        if self.isTicked == False and len(list(filter(None.__ne__, self.stateHashes))) <= 1:
            self.isTicked = None
            return

        # Start tracking if sufficient observation span is reached
        if self.__minSpan >= 1 and self.isTicked != True:
            entryLocs = [i for i, value in enumerate(self.stateHashes) if value != None]
            if entryLocs[-1]-entryLocs[0] > self.__minSpan:
                self.isTicked = False
                return
            
            # May be triggered if a system has two observation close to eachother
            self.isTicked = None
            return






    def receiveStateUpdate(self, hash: int):
        # State is already present in log (a normal Update)
        if hash in self.stateHashes:
            self.stateHashes[(self.__maxIntvlCnt-1)] = hash
            self.intrvlsSinceUpdate = 0
            return
        
        # State is entirely new (a Tick has occurred)
        self.stateHashes[(self.__maxIntvlCnt-1)] = hash
        self.isTicked = True
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0

        # NB: This doesn't report a Tick on the System's first entry, because first entry is part of the __init__