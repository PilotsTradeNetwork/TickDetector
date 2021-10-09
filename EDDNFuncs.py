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

    def run(self, filterType: str = "Influence"):
        schemaURL = 'https://raw.githubusercontent.com/EDCD/EDDN/master/schemas/journal-v1.0.json'
        setupEDDN()
        with urllib.request.urlopen(schemaURL) as url:
            data = simplejson.loads(url.read().decode())

        schema = data
        expression = regex.compile('("Influence": \d+\.\d+)')
        while True:
            time.sleep(0) # maybe move me to the end of the list
            eventJson = listenEDDN()

            # Validate event schema
            try:
                validate(eventJson, schema=schema)
            except Exception as e:
                # print(e)
                continue
            
            event = EListn.createFSDJumpEvent(EListn.createMessageFromJson(eventJson))

            if event == None or event.eventAgeSeconds > 300 or event.factions == None:
                continue
            
            # This will detect influence or state tick changes in a system
            if filterType == "Influence":
                textInf = ''.join(regex.findall('("Influence": \d+\.\d+)', simplejson.dumps(event.factions)))
                # print(f"Test: {textInf}")
                hashVal = hash(textInf)
                systemName = event.systemName

            #bug fixing
            # if systemName == "Alcor":
            #     print(simplejson.dumps(event.factions))
            
            # Guard for empty sysList
            if len(systemList) == 0:
                systemList.append(System(systemName, hashVal))
                continue
            
            for sys in systemList:
                if sys.name == systemName:
                    sys.receiveStateUpdate(hashVal)
                    continue
            
            # add a new system to sysList
            systemList.append(System(systemName, hashVal))

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