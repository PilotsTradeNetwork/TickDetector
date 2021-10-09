from datetime import datetime
from threading import Thread
import time
from system import systemList



class iteratorThread(Thread):

    def run(self, intervalMins: int = 5):
        global systemList
        sleepTime = intervalMins * 60

        while True:
            time.sleep(sleepTime)
            #   iterate over system list
            #   remove entries marked for deletion
            #   execute iteration step on each entry
            print("Iteration beginning")
            systemList = [sys for sys in systemList if sys.performInterval() == False]
            self.__printTracking(systemList)

            # do thing (send the info somewhere useful, like push to discord or do a webhook thing or update a website)

    def __printTracking(self, systemList):
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
        now = datetime.now()
        nowFormatted = now.strftime("%H:%M:%S")
        print(f"Ticked Systems = {ticked},\nTracked Systems = {tracked},\nObserved Systems = {observed}")
