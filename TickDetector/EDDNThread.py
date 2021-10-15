from threading import Thread
import zlib
import zmq
import simplejson
from jsonschema import validate
import sys as sysImport
import time
import urllib.request
import re as regex

import EDDNEventListenerModule as EListn
from settings import EDDN_RELAY, JOURNAL_SCHEMA_URL
from SystemManager import systemManager as sysMan

class EDDNThread(Thread):
    def __init__(self):
        super().__init__()

        # Get journal event schema from EDDN directly
        with urllib.request.urlopen(JOURNAL_SCHEMA_URL) as url:
            schemaData = simplejson.loads(url.read().decode())
        self.schema = schemaData
        
        # Regex expression for extracting Influence values from textual json
        self.influenceRegex = regex.compile('("Influence": \d+\.\d+)')

        # ZMQ stuff
        self.__subscriber = None
        self.__timeoutEDDN = 600000
        
        self.__setupEDDN()
        
        print("EDDNThread started")
        
    def run(self):
        global sysMan

        while True:
            time.sleep(0) # Allow iteratorThread to run without them running simultaneously

            eventJson = self.listenEDDN()

            try:
                validate(eventJson, schema=self.schema) # validate comes from jsonschema
            except Exception:
                continue
            
            event = EListn.createFSDJumpEvent(EListn.createMessageFromJson(eventJson))

            # Skip non FSDJumps, old updates (>5min), and factionless (unpopulated) systems
            if event == None or event.eventAgeSeconds > 300 or event.factions == None:
                continue
            
            # Convert factions list to json object for hashing
            influenceText = ''.join(regex.findall(self.influenceRegex, simplejson.dumps(event.factions)))
            hashVal = hash(influenceText)
            sysName = event.systemName

            sysMan.updateSystemList(hashVal, sysName)

    def __setupEDDN(self):
            global __subscriber
            context     = zmq.Context()
            self.__subscriber  = context.socket(zmq.SUB)
            
            self.__subscriber.setsockopt(zmq.SUBSCRIBE, b"")
            self.__subscriber.setsockopt(zmq.RCVTIMEO, self.__timeoutEDDN)

    def listenEDDN(self):
        try:
            self.__subscriber.connect(EDDN_RELAY)
            sysImport.stdout.flush()
            __message = self.__subscriber.recv()
            if __message == False:
                self.__subscriber.disconnect(EDDN_RELAY)
                return None
            __message   = zlib.decompress(__message)
            __json      = simplejson.loads(__message)
            return __json

        except zmq.ZMQError as e:
            print ('ZMQSocketException: ' + str(e))
            sysImport.stdout.flush()
            self.__subscriber.disconnect(EDDN_RELAY)
            time.sleep(5)