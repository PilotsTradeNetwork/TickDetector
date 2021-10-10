from datetime import datetime
from threading import Thread
import time
from system import systemList



class iteratorThread(Thread):

    def __init__(self, intervalMins: int = 5):
        super().__init__()
        self.intrvlMins = intervalMins * 60

    def run(self):
        global systemList

        while True:
            time.sleep(self.intrvlMins)
            #   iterate over system list
            #   remove entries marked for deletion
            #   execute iteration step on each entry
            print("\nIteration beginning")
            systemList[:] = [sys for sys in systemList if not sys.performInterval()]
            self.__printTracking(systemList)

            # do thing (send the info somewhere useful, like push to discord or do a webhook thing or update a website)

    def __printTracking(self, systemList):
        tracked = 0
        observed = 0
        ticked = 0

        for sys in systemList:
            if sys.isTicked == True:
                ticked += 1
                tracked += 1
                observed += 1
            elif sys.isTicked == False:
                tracked += 1
                observed += 1
            elif sys.isTicked == None:
                observed += 1
        now = datetime.now()
        nowFormatted = now.strftime("%H:%M:%S")
        print(f"Time: {nowFormatted}\nTicked Systems in last Hr = {ticked},\nCurrently Tracked Systems = {tracked},\nCurrently Observed Systems = {observed}")
