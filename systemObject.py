class System:
    def __init__(self, name: str):
        self.name = name
        self.hashedStates = [None]*12
        self.ticked = None
        self.intervalsSinceTick = 0


    # Public Functions

    # Called every 5 minutes
    def interval(self):
        self.hashedStates = self.hashedStates[1:11]
        self.hashedStates.append(None)

        if self.ticked == True:
            self.intervalsSinceTick += 1

            # Unticks system after 1hr
            if self.intervalsSinceTick >= 12:
                self.ticked = False


    def receiveStateUpdate(self, hashVal: int):
        if self.hashedStates[11] == hashVal:
            return
        
        # Only reached if system ticks
        self.hashedStates[11] = hashVal
        self.ticked = True
        self.intervalsSinceTick = 0

    def checkTicked(self):
        entries = list(set(self.hashedStates))
        entries.remove(None)
        if len(entries) > 1:
            return True
        return False