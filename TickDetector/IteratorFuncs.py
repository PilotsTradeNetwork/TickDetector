from datetime import datetime
from threading import Thread
import time
from system import systemList
from privateInfo import TEST_DISCORDWEBHOOKURL
from discord_webhook import DiscordWebhook



class iteratorThread(Thread):
    global systemList

    def __init__(self, intervalMins: int = 5):
        super().__init__()
        self.__intrvl = intervalMins * 60
        
        self.__tracked = 0
        self.__observed = 0
        self.__ticked = 0
        
        print("IteratorThread started")

    def run(self):
        while True:
            time.sleep(self.__intrvl)
            print("\nIteration beginning...")

            # Deletes systems according to performInterval's logic
            systemList[:] = [sys for sys in systemList if sys.performInterval()]

            self.__printTracking(systemList)

            self.__sendStatusToDiscord()

    def __printTracking(self, systemList):
        self.__tracked = 0
        self.__observed = 0
        self.__ticked = 0

        for sys in systemList:
            if sys.isTicked == True:
                self.__ticked += 1
                self.__tracked += 1
                self.__observed += 1
            elif sys.isTicked == False:
                self.__tracked += 1
                self.__observed += 1
            elif sys.isTicked == None:
                self.__observed += 1
        
        now = datetime.now()
        nowFormatted = now.strftime("%H:%M:%S")
        print(f"Time: {nowFormatted}\nTicked Systems in last Hr = {self.__ticked},\nCurrently Tracked Systems = {self.__tracked},\nCurrently Observed Systems = {self.__observed}")

    def __sendStatusToDiscord(self):
        webhook = DiscordWebhook(url=TEST_DISCORDWEBHOOKURL, content=f'Tracked Systems: {self.__tracked}\nTicked Systems: {self.__ticked}')
        response = webhook.execute()

