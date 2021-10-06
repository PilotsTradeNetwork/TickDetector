

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

        # Move tracking window along and add empty slot for new data
        self.stateHashes = self.stateHashes[1:(self.__maxIntvlCnt-1)]
        self.stateHashes.append(None)
        
        # Handle untracked, entirely out of date systems
        # Delete the object if it has no data
        if self.isTicked == None and self.intrvlsSinceUpdate >= self.__maxIntvlCnt:
            self.deletionMark = True
            #TODO: Should this function return a bool instead of updating the deletionMark? Ans: yes :)
            return True

        # Handle 'Ticked' Systems
        if self.isTicked == True:
            self.intrvlsSinceTick += 1

            if self.intrvlsSinceTick >= self.__maxIntvlCnt:
                self.isTicked = False
                self.intrvlsSinceTick = 0
                #NB: lack of return statement here, will continue to 3rd if
            else:
                # This return 'keeps' systems that ticked in the last hour, regardless of data freshness
                return False
        
        # Screening unticked systems with insufficient data
        # Start tracking if sufficient observation span is reached
        if self.intrvlsSinceUpdate >= self.__minSpan:
            self.isTicked = None
            return False
        
        # No changes need to be made (?)
        return False

    def receiveStateUpdate(self, hash: int):
        """Accepts a hash of a system's state, handles whether that represents a new tick and flags it."""
        # State is already present in log (a normal Update), and current interval has not been updated
        if self.intrvlsSinceUpdate > 0 and hash in self.stateHashes:
            self.stateHashes[(self.__maxIntvlCnt-1)] = hash
            self.intrvlsSinceUpdate = 0
            return
        
        # State is entirely new (a Tick has occurred)
        self.stateHashes[(self.__maxIntvlCnt-1)] = hash
        self.isTicked = True
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0

        # NB: This doesn't report a Tick on the System's first entry, because first entry occurs as part of the __init__