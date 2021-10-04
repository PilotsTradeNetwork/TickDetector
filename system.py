class System:
    def __init__(self, name: str, hashVal: int, maxIntervalCount: int, deletionInterval: int):
        # unique identifier
        self.name = name


        self.hashedStates = [None]*11
        self.hashedStates.append(hashVal)

        self.maxIntvlCnt = maxIntervalCount
        self.dltIntrvl = deletionInterval

        # state
        self.ticked = None
        self.intrvlsSinceTick = 0
        self.intrvlsSinceUpdate = 0

        self.deletionMark = False

    # Called every 5 minutes
    def interval(self):
        """Performs the system's status management, designed to work on 5 minute intervals."""
        self.hashedStates = self.hashedStates[1:(self.maxIntvlCnt-1)]
        self.hashedStates.append(None)

        if self.ticked == True:
            self.intrvlsSinceTick += 1

            # Unticks system after 1hr
            if self.intrvlsSinceTick >= self.maxIntvlCnt:
                self.ticked = False
        
        self.intrvlsSinceUpdate += 1
        if self.intrvlsSinceUpdate >= self.dltIntrvl:
            self.deletionMark = True


    def receiveStateUpdate(self, hashVal: int):
        # if updateState is already most current
        if self.hashedStates[(self.maxIntvlCnt-1)] == hashVal:
            return
        
        # State is already present but not most current
        if hashVal in self.hashedStates:
            self.hashedStates[(self.maxIntvlCnt-1)] = hashVal
            return
        
        # State is entirely new
        self.hashedStates[(self.maxIntvlCnt-1)] = hashVal
        self.ticked = True
        self.intrvlsSinceTick = 0