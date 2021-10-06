from threading import Thread
import time
from main import systemList



class iteratorThread(Thread):
    global systemList

    def run(self, intervalMins: int = 5):

        sleepTime = intervalMins * 60


        while True:
            time.sleep(sleepTime)
            #   iterate over system list
            #   remove entries marked for deletion
            #   execute iteration step on each entry
            systemList[:] = [sys for sys in systemList if sys.performInterval()]
            self.__printTracking(systemList)

            # do thing (send the info somewhere useful, like push to discord or do a webhook thing or update a website)

    def __printTracking(systemList):
            tracked = 0
            observed = 0
            ticked = 0
            for sys in systemList:
                if sys.isTicked == True:
                    ticked += 1
                elif sys.isTicked == False:
                    tracked += 1
                elif sys.isTicked == None:
                    observed += 1
                continue
            print("Time: {T}Ticked Systems = {ticked},\nTracked Systems = {tracked},\nObserved Systems = {observed}")
