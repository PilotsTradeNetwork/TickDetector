import zlib
import zmq
import simplejson
import sys
import time
import threading

# my libs
from system import System

from zmq.sugar.constants import NULL

__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000
__subscriber            = None

def main():
    # 2 threads
    # EDDN facing thread
    #   get message
    #       filter by:
    #       schema
    #       isPopulated
    #       has a faction
    #   form a factions object
    #   hash the factions object
    #   pass the hash and its system to system list

    # 5 min interval update thread
    #   iterate over system list
    #       remove entries marked for deletion
    #       execute iteration step on each entry

    setupEDDN()
    while True:
        __json = listenEDDN()


    return None




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

if __name__ == '__main__':
    main()