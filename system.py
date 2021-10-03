class System:
    def __init__(self, name: str, hashVal: int):
        # unique identifier
        self.name = name


        self.hashedStates = [None]*11
        self.hashedStates.append(hashVal)


        self.ticked = None
        self.intervalsSinceTick = 0
        self.intervalsSinceUpdate = 0

        self.deletionMark = False

    # Called every 5 minutes
    def interval(self):
        """Performs the system's status management, designed to work on 5 minute intervals."""
        self.hashedStates = self.hashedStates[1:11]
        self.hashedStates.append(None)

        if self.ticked == True:
            self.intervalsSinceTick += 1

            # Unticks system after 1hr
            if self.intervalsSinceTick >= 12:
                self.ticked = False
        
        self.intervalsSinceUpdate += 1
        if self.intervalsSinceUpdate == 5:
            self.deletionMark = True


    def receiveStateUpdate(self, hashVal: int):
        # if updateState is already most current
        if self.hashedStates[11] == hashVal:
            return
        
        # State is already present but not most current
        if hashVal in self.hashedStates:
            self.hashedStates[11] = hashVal
            return
        
        # State is entirely new
        self.hashedStates[11] = hashVal
        self.ticked = True
        self.intervalsSinceTick = 0