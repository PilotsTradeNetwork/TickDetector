from threading import Thread
import zlib
import zmq
import simplejson
from jsonschema import validate
import sys
import time
from urllib.request import urlopen
from system import System

import EDDNEventListenerModule as EListn
from main import systemList

__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000
__subscriber            = None
__schemaURL             = 'https://raw.githubusercontent.com/EDCD/EDDN/master/schemas/journal-v1.0.json'


class EDDNThread(Thread):
    global systemList
    def run(self, filterType: str):
        self.__setupEDDN()
        schema = simplejson.loads(urlopen(__schemaURL))
        while True:
            time.sleep(0) # maybe move me to the end of the list
            eventJson = self.__listenEDDN()

            # Validate event schema
            try:
                validate(eventJson, schema=schema)
            except Exception as e:
                print(e)
                continue
            
            event = EListn.FSDJumpEvent(EListn.createMessageFromJson(eventJson))

            if event == None or event.eventAgeSeconds > 300 or event.systemPopulation < 1 or event.factions == None:
                continue
            
            hashVal = hash(event.messageData.get('Factions'))
            systemName = event.systemName
            if len(systemList) == 0:
                systemList.append(System(systemName, hashVal))
                continue
            for sys in systemList:
                if sys.name == systemName:
                    sys.receiveStateUpdate(hashVal)
                    continue
            systemList.append(System(systemName, hashVal))
            # filter b
            # filter c
            # hashing function
            # update or create a system

    def __setupEDDN():
        global __subscriber
        context     = zmq.Context()
        __subscriber  = context.socket(zmq.SUB)
        
        __subscriber.setsockopt(zmq.SUBSCRIBE, b"")
        __subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)


    def __listenEDDN():
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