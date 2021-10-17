from datetime import datetime
from threading import Thread
import time
from discord_webhook import DiscordWebhook
from settings import WEBHOOK_URL, INTERVAL_DURATION_MINS
from SystemManager import systemManager as sysMan

class IteratorThread(Thread):
    def __init__(self):
        super().__init__()
        self.__intrvl = INTERVAL_DURATION_MINS * 60
        self.__ticked = self.__tracked = self.__observed = 0
        print("IteratorThread started")

    def run(self):
        global sysMan
        while True:
            time.sleep(self.__intrvl)
            print("\nIteration beginning...")

            sysMan.iterateSystemList() #Most important line in this function

            self.__calculateTracking(sysMan.systemList)

            self.__printStatus()

            self.__sendStatusToDiscord()

    def __calculateTracking(self, sysL):
        """Counts up Systems according to their status, takes the SystemList."""
        self.__ticked = self.__tracked = self.__observed = 0

        for sys in sysL:
            if sys.isTicked == True:
                self.__ticked += 1
            if sys.isTicked is not None:
                self.__tracked += 1
            
            self.__observed += 1 # All systems in the system list are observed at minimum

        #TODO: Consider moving into SystemManager, and returning tick/track/obs variables

    def __printStatus(self):
        now = datetime.now()
        nowFormatted = now.strftime("%H:%M:%S")
        print(f"Time: {nowFormatted}\nTicked Systems in last Hr = {self.__ticked},\n"\
            f"Currently Tracked Systems = {self.__tracked},\nCurrently Observed Systems = {self.__observed}")

    def __sendStatusToDiscord(self):
        webhook = DiscordWebhook(url=WEBHOOK_URL, content=f'Tracked Systems: {self.__tracked}\nTicked Systems: {self.__ticked}')
        response = webhook.execute()
