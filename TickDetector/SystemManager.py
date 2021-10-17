from System import System
from settings import MAX_INTERVALS, MIN_INTERVAL_FREQUENCY

class SystemManager:
    def __init__(self, maxIntervals: int = 12, minFrequencyToTrack: int = 6):
        if minFrequencyToTrack >= maxIntervals:
            raise ValueError(f'Minimum Interval to Track param\''\
                f' ({minFrequencyToTrack}) must be smaller than the Maximum Interval param\' ({maxIntervals})')
        
        self.systemList = []
        self.__maxIntervalCount = MAX_INTERVALS
        self.__minFrequency = MIN_INTERVAL_FREQUENCY

    def iterateSystemList(self):
        """Handles the interval-bound updating, tracking, and deletion of System objects."""
        self.systemList[:] = [sys for sys in self.systemList if self._iterateSystem(sys)]

    def updateSystemList(self, hashVal: int, sysName: str):
        existingSysIndex = self.__findExistingSystem(sysName)

        if existingSysIndex == None:
            self.systemList.append(System(sysName, hashVal, self.__maxIntervalCount))
        else:
            self._updateSystem(self.systemList[existingSysIndex], hashVal)

    def _updateSystem(self, sys: System, hashVal: int):
        """Accepts a hash of a system's faction's overall state, handles whether that represents a new tick."""
        if sys.intrvlsSinceUpdate > 0:
            if hashVal in sys.hashes:
                self.__receiveStateUpdate(sys, hashVal)
            else:
                self.__receiveStateChange(sys, hashVal)
        else:
            return
        
        # NB: This doesn't report a Tick on the System's first entry, because first entry occurs as part of the __init__

    def __receiveStateChange(self, sys: System, hash: int):
        # State is entirely new (a Tick has occurred)
        sys.hashes[(self.__maxIntervalCount-1)] = hash
        sys.isTicked = True
        sys.intrvlsSinceTick = 0
        sys.intrvlsSinceUpdate = 0
        # print(f"System {sys.name}'s faction influence has changed.")

    def __receiveStateUpdate(self, sys: System, hash: int):
        # State is already present in log (a normal Update), and current interval has not been updated
        sys.hashes[(self.__maxIntervalCount-1)] = hash
        sys.__intrvlsSinceUpdate = 0
        if sys.isTicked == None:
            sys.isTicked = False
        # print(f"System {self.name} received an update.")

    def _iterateSystem(self, sys: System):
        """Performs a system's status management - returns whether the system object should be deleted."""
        sys.intrvlsSinceUpdate += 1

        # Move tracking window along and add empty slot for new data
        sys.hashes.pop(0)
        sys.hashes.append(None)

        if sys.intrvlsSinceUpdate >= self.__maxIntervalCount:
            # System has no data, it will be deleted
            return False

        self.__iterateIfTicked(sys)
        self.__iterateIfExpired(sys)

        # System has data and will therefore be kept
        return True

    def __findExistingSystem(self, reportedSysName: str):
        """Finds existing systems if they are in the list, otherwise returns None."""
        if len(self.systemList) > 0:
            for index, sys in enumerate(self.systemList):
                if sys.name == reportedSysName:
                    return index
        return None

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

systemManager = SystemManager()