from threading import Thread
import time
from system import System
from __future__ import annotations
systemList = [System]


class iteratorThread(Thread):
    def run(self, intervalMins: int):

        sleepTime = intervalMins * 60
        global systemList


        while True:
            time.sleep(sleepTime)

            #   iterate over system list
            #   remove entries marked for deletion
            #   execute iteration step on each entry
            systemList[:] = [sys for sys in systemList if sys.performInterval()]
        return