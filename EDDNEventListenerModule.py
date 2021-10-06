import datetime
import re as regex

def createMessageFromJson(jsonData):
    """Wrapper that gets the 'message' data structure from jsonData received by EDDN"""
    try:
        message = jsonData['message']
        return message
    except Exception as e:
        print("getMessageData() jsonData that does not contain the 'message' datastructure found:")
        print(e)
    return None


def formatTimestamp(rawTimestamp):
    regexPattern = r"(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2}:\d{2})."
    
    cleanTimestampArr = regex.split(regexPattern, rawTimestamp)
    dateTimeString = cleanTimestampArr[1] + " " + cleanTimestampArr[2] + ".000000"
    cleanTimeStamp = datetime.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S.%f')
    return cleanTimeStamp


class Event:
    def __init__(self, message):
        self.timestamp = message.get('timestamp')
        self.formattedTimestamp = formatTimestamp(self.timestamp)
        self.eventAgeSeconds = (datetime.datetime.utcnow() - self.formattedTimestamp).seconds
        self.eventType = message.get('event')
        if self.eventType == None:
            raise ValueError("Class 'Event': attempted to instantiate an Event Object using a message containing no Event. Check if the message has an event first.")

def createFSDJumpEvent(message):
    if message == None: 
        return None

    if message.get('event') == 'FSDJump':
        return FSDJumpEvent(message)
    return None


class FSDJumpEvent(Event):
    """FSDJumpEvent class, an OOP approach, extends EDDNEvent"""
    def __init__(self, message):
        super().__init__(message)
        # Jump data
        self.fuelUsed = message.get('FuelUsed')
        self.fuelLevel = message.get('FuelLevel')
        self.boostUsed = message.get('BoostUsed')

        # System data that's always present
        self.systemName = message.get('StarSystem')
        if self.systemName == None:
            # Backup data location
            self.systemName = message.get('SystemAddress')

        self.systemBody = message.get('Body')
        self.systemCoordinates = message.get('StarPos')
        self.systemPopulation = message.get('Population')
        self.systemSecurity = message.get('SystemSecurity')

        # only present/relevant in populated systems
        self.systemAllegiance = message.get('SystemAllegiance')
        self.systemEconomy = message.get('SystemEconomy')
        self.systemSecondEconomy = message.get('SystemSecondEconomy')
        self.systemGovernment = message.get('SystemGovernment')

        # Faction stuff, probably all needs revalidating due to data nesting
        self.controllingFactionName = message.get('SystemFaction') # MAYBE REDUNDANT
        self.factions = getFactions(message)

        # Message Data
        self.messageData = message

def getFactions(message):
    systemFactions = message.get('Factions')
    if systemFactions == None:
        return None
    else:
        try:
            controllingFactionName = message['SystemFaction'].get('Name')
        except AttributeError as a:
            print(f"Unusually formed controlling faction name encountered: {a}\n{message}")
        
        # The above catch wasn't sufficient for all cases, the below statement resolves remaining errors
        # It can be hard to test this, as systems containing such 'malformed' factions are rarely jumped into
        # I believe it's primarily prison systems
        # TODO: maybe make this if part of the exception, or the try statement
        if 'controllingFactionName' not in locals():
            controllingFactionName = None
        
        warInfo = None
        if 'Conflicts' in message:
            warInfo = message['Conflicts']
        factionList = []
        for faction in systemFactions:
            factionList.append(Faction(faction, controllingFactionName, warInfo))
        return factionList

class Faction:
    # faction class which encapsulates all faction-pertinent data
    def __init__(self, factionInfo, controllingFactionName, warInfo):
        # basic bitch shit
        self.name = factionInfo.get('Name')
        self.state = factionInfo.get('FactionState')
        self.governmentType = factionInfo.get('Government')
        self.influenceDecimal = round(factionInfo.get('Influence'), 2)
        self.happiness = factionInfo.get('Happiness')

        # states
        self.pendingStates = self.__getStates(factionInfo.get('PendingStates', None))
        self.recoveringStates = self.__getStates(factionInfo.get('RecoveringStates', None))
        self.activeStates = self.__getStates(factionInfo.get('ActiveStates', None)) # YOU REALLY WANT THESE

        self.controllingFlag = True if controllingFactionName == self.name else False

        # war info would go here
        self.warOpponent = None
    
    def __getStates(self, stateDict):
        if stateDict == None:
            return None
        stateList = []
        for state in stateDict:
            # returns a tuple of the state name, and its trend value (if applicable, otherwise trend is None)
            if 'Trend' in state:
                stateList.append((state['State'], state['Trend']))
            elif 'State' in state:
                stateList.append((state['State'], None))
        return stateList

    def listStateNames(self, stateType: str):
        """Returns a list of active states for a single faction depending on the state type desired: 'active', 'pending', and 'recovering'"""
        stateList = []
        if stateType == 'active':
            if self.activeStates == None:
                return None
            for state in self.activeStates:
                stateList.append(state[0])
        elif stateType == 'pending':
            if self.pendingStates == None:
                return None
            for state in self.pendingStates:
                stateList.append(state[0])
        elif stateType == 'recovering':
            if self.recoveringStates == None:
                return None
            for state in self.recoveringStates:
                stateList.append(state[0])
        return stateList