from System import System
from TickDetector import system

class SystemManager:
    def __init__(self, maxIntervals: int = 12, minFrequencyToTrack: int = 6):
        if minFrequencyToTrack >= maxIntervals:
            raise ValueError(f'Minimum Interval to Track param\' ({minFrequencyToTrack}) must be smaller than the Maximum Interval param\' ({maxIntervals})')
        self.systemList = []
        self.__maxIntervalCount = maxIntervals
        self.__minFrequency = minFrequencyToTrack

    def iterateSystems(self):
        # Deletes systems according to performInterval's logic
        self.systemList[:] = [sys for sys in self.systemList if self.performInterval(sys)]

    def performInterval(self, sys: System):
        """Performs a system's status management - returns whether the system object should be deleted."""
        sys.intrvlsSinceUpdate += 1

        # Move tracking window along and add empty slot for new data
        sys.hashes.pop(0)
        sys.hashes.append(None)

        if sys.__intrvlsSinceUpdate >= self.__maxIntervalCount:
            # System has no data, it will be deleted
            return False

        # Handle 'Ticked' Systems
        self.__iterateIfTicked(sys)
        self.__iterateIfExpired(sys)

        # System has data and will therefore be kept
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

    def __iterateIfTicked(self, sys: System):
        # Handle 'Ticked' Systems
        if sys.isTicked == True:
            sys.intrvlsSinceTick += 1
            if sys.intrvlsSinceTick >= self.__maxIntervalCount:
                # The point of this return is to ensure a ticked system remains tracked until the tick state goes out of scope
                
                sys.isTicked = False
                sys.intrvlsSinceTick = 0

    def __iterateIfExpired(self, sys: System):
        if not sys.isTicked:
            if sys.intrvlsSinceUpdate >= self.__minFrequency and sys.isTicked == False:
                sys.isTicked = None

    def __receiveStateUpdate(self, sys: System, hash: int):
        # State is already present in log (a normal Update), and current interval has not been updated
        sys.hashes[(self.__maxIntervalCount-1)] = hash
        self.__intrvlsSinceUpdate = 0
        if self.isTicked == None:
            self.isTicked = False
        # print(f"System {self.name} received an update.")
    
    def __receiveStateChange(self, sys: System, hash: int):
        # State is entirely new (a Tick has occurred)
        sys.hashes[(self.__maxIntervalCount-1)] = hash
        sys.isTicked = True
        sys.intrvlsSinceTick = 0
        sys.intrvlsSinceUpdate = 0
        print(f"System {sys.name}'s faction influence has changed.")

        def __updateSystemList(self, hashVal: int, sysName: str):
        existingIndex = self.__findExistingSystem(sysName)

        if existingIndex == None:
            systemList.append(System(sysName, hashVal, self.maxObsIntrvls, self.minSpan))
        else:
            systemList[existingIndex].receiveStateUpdate(hashVal)


    def __findExistingSystem(self, reportedSysName):
        """Finds existing systems if they are in the list, otherwise returns None."""
        if len(systemList) > 0:
            for index, system in enumerate(systemList):
                if system.name == reportedSysName:
                    return index
        return None