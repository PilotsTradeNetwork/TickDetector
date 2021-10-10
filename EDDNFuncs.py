from threading import Thread
import zlib
import zmq
import simplejson
from jsonschema import validate
import sys
import time
import urllib.request
import re as regex

import EDDNEventListenerModule as EListn
from system import systemList, System

__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000
__subscriber            = None


class EDDNThread(Thread):
    global systemList

    def __init__(self, maxIntervals: int = 12, minFrequencyToTrack: int = 6):
        super().__init__()
        if minFrequencyToTrack >= maxIntervals:
            raise ValueError(f'Minimum Interval to Track param\' ({minFrequencyToTrack}) must be smaller than the Maximum Interval param\' ({maxIntervals})')

        # Variables to control interval window
        self.maxObsIntrvls = maxIntervals
        self.minSpan = minFrequencyToTrack

        # Get journal event schema from EDDN directly
        schemaURL = 'https://raw.githubusercontent.com/EDCD/EDDN/master/schemas/journal-v1.0.json'
        with urllib.request.urlopen(schemaURL) as url:
            schemaData = simplejson.loads(url.read().decode())
        self.schema = schemaData
        
        # Regex expression for extracting Influence values from textual json
        self.influenceRegex = regex.compile('("Influence": \d+\.\d+)')
        
        setupEDDN()
        
    def run(self):
        while True:
            time.sleep(0) # Allow iteratorThread to run without them running simultaneously

            eventJson = listenEDDN()

            try:
                validate(eventJson, schema=self.schema) # validate comes from jsonschema
            except Exception:
                continue
            
            event = EListn.createFSDJumpEvent(EListn.createMessageFromJson(eventJson))

            # skip non FSDJumps, old updates (>5min), and factionless (unpopulated) systems
            if event == None or event.eventAgeSeconds > 300 or event.factions == None:
                continue
            
            # Convert factions list to json object for hashing
            influenceText = ''.join(regex.findall(self.influenceRegex, simplejson.dumps(event.factions)))
            hashVal = hash(influenceText)
            sysName = event.systemName
            
            if self.__isExistingSystem(sysName, hashVal):
                continue
            else:
                systemList.append(System(sysName, hashVal, self.maxObsIntrvls, self.minSpan))

    def __isExistingSystem(self, reportedSysName, hashVal):
        if len(systemList) > 0:
            for system in systemList:
                if system.name == reportedSysName:
                    system.receiveStateUpdate(hashVal)
                    return True
        return False


def setupEDDN():
        global __subscriber
        context     = zmq.Context()
        __subscriber  = context.socket(zmq.SUB)
        
        __subscriber.setsockopt(zmq.SUBSCRIBE, b"")
        __subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)


def listenEDDN():
        try:
            __subscriber.connect(__relayEDDN)
            sys.stdout.flush()
            __message   = __subscriber.recv()
            if __message == False:
                __subscriber.disconnect(__relayEDDN)
                return None
            __message   = zlib.decompress(__message)
            __json      = simplejson.loads(__message)
            return __json

        except zmq.ZMQError as e:
            print ('ZMQSocketException: ' + str(e))
            sys.stdout.flush()
            __subscriber.disconnect(__relayEDDN)
            time.sleep(5)

# EDDN facing thread
#   get message
#       filter by:
#       schema
#       isPopulated
#       has a faction
#   form a factions object
#   hash the factions object
#   pass the hash and its system to system list