import datetime
import re as regex

def createMessageFromJson(jsonData):
    """Wrapper that gets the 'message' data structure from jsonData received by EDDN"""
    try:
        message = jsonData['message']
        return message
    except Exception as e:
        print(f"jsonData that does not contain the 'message' datastructure found:\n{e}")

    return None


class Event:
    def __init__(self, message):
        self.__eventRawTimestamp = message.get('timestamp')
        self.formattedTimestamp = _formatTimestamp(self.__eventRawTimestamp)
        self.eventAgeSeconds = (datetime.datetime.utcnow() - self.formattedTimestamp).seconds
        self.eventType = message.get('event')
        if self.eventType == None:
            raise ValueError("Class 'Event': attempted to instantiate an Event Object using a \
                            message containing no Event. Check if the message has an event first.")

def createFSDJumpEvent(message):
    if message.get('event') == 'FSDJump':
        return FSDJumpEvent(message)
    
    return None

class FSDJumpEvent(Event):
    """Extends Event class. This is a lightweight version of FSDJumpEvent"""
    def __init__(self, message):
        super().__init__(message)

        if self.eventType != 'FSDJump':
            raise ValueError('FSDJump event cannot be created from non-FSDJump data')

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

def _formatTimestamp(unformattedTimestamp):
    regexPattern = r"(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2}:\d{2})."
    
    cleanTimeStampArr = regex.split(regexPattern, unformattedTimestamp)
    if cleanTimeStampArr == None:
        raise ValueError(f"An incorrectly formatted timestamp was received\n{unformattedTimestamp}")

    dateTimeString = cleanTimeStampArr[1] + " " + cleanTimeStampArr[2] + ".000000"
    cleanTimeStamp = datetime.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S.%f')
    return cleanTimeStamp

