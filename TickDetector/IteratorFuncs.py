from datetime import datetime
from threading import Thread
import time
from system import systemList
from discord_webhook import DiscordWebhook
from settings import WEBHOOK_URL

class iteratorThread(Thread):
    global systemList

    def __init__(self, intervalMins: int = 5):
        super().__init__()
        self.__intrvl = intervalMins * 60
        self.__ticked = self.__tracked = self.__observed = 0
        print("IteratorThread started")

    def run(self):
        while True:
            time.sleep(self.__intrvl)
            print("\nIteration beginning...")

            # Deletes systems according to performInterval's logic
            systemList[:] = [sys for sys in systemList if sys.performInterval()]

            self.__calculateTracking()

            self.__printStatus()

            self.__sendStatusToDiscord()

    def __calculateTracking(self):
        self.__ticked = self.__tracked = self.__observed = 0

        for sys in systemList:
            if sys.isTicked == True: self.__ticked += 1
            if sys.isTicked is not None: self.__tracked += 1
            self.__observed += 1

    def __printStatus(self):
        now = datetime.now()
        nowFormatted = now.strftime("%H:%M:%S")
        print(f"Time: {nowFormatted}\nTicked Systems in last Hr = {self.__ticked},\n"\
            f"Currently Tracked Systems = {self.__tracked},\nCurrently Observed Systems = {self.__observed}")

    def __sendStatusToDiscord(self):
        webhook = DiscordWebhook(url=WEBHOOK_URL, content=f'Tracked Systems: {self.__tracked}\nTicked Systems: {self.__ticked}')
        response = webhook.execute()
