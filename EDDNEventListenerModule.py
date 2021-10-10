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



class Event:
    def __init__(self, message):
        self.timestamp = message.get('timestamp')
        self.formattedTimestamp = self.__formatTimestamp(self.timestamp)
        self.eventAgeSeconds = (datetime.datetime.utcnow() - self.formattedTimestamp).seconds
        self.eventType = message.get('event')
        if self.eventType == None:
            raise ValueError("Class 'Event': attempted to instantiate an Event Object using a message containing no Event. Check if the message has an event first.")

    def __formatTimestamp(rawTimestamp):
        regexPattern = r"(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2}:\d{2})."
        
        cleanTimestampArr = regex.split(regexPattern, rawTimestamp)
        dateTimeString = cleanTimestampArr[1] + " " + cleanTimestampArr[2] + ".000000"
        cleanTimeStamp = datetime.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S.%f')
        return cleanTimeStamp

def createFSDJumpEvent(message):
    if message == None: 
        return None

    if message.get('event') == 'FSDJump':
        return FSDJumpEvent(message)
    return None

class FSDJumpEvent(Event):
    """FSDJumpEvent, but super lightweight"""
    def __init__(self, message):
        super().__init__(message)

        # System data that's always present
        self.systemName = message.get('StarSystem')
        if self.systemName == None:
            # Backup data location
            self.systemName = message.get('SystemAddress')
        self.systemCoordinates = message.get('StarPos')
        self.systemPopulation = message.get('Population')
        self.factions = message.get('Factions')
        
        # Message Data
        #self.messageData = message