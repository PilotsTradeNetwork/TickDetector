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
        self.intrvlMins = intervalMins * 60
        
        self.tracked = 0
        self.observed = 0
        self.ticked = 0

    def run(self):
        while True:
            time.sleep(self.intrvlMins)
            #   iterate over system list
            #   remove entries marked for deletion
            #   execute iteration step on each entry
            print("\nIteration beginning")
            systemList[:] = [sys for sys in systemList if not sys.performInterval()]
            self.__printTracking(systemList)
            self.__sendStatusToDiscord()

            # do thing (send the info somewhere useful, like push to discord or do a webhook thing or update a website)

    def __printTracking(self, systemList):
        self.tracked = 0
        self.observed = 0
        self.ticked = 0

        for sys in systemList:
            if sys.isTicked == True:
                self.ticked += 1
                self.tracked += 1
                self.observed += 1
            elif sys.isTicked == False:
                self.tracked += 1
                self.observed += 1
            elif sys.isTicked == None:
                self.observed += 1
        now = datetime.now()
        nowFormatted = now.strftime("%H:%M:%S")
        print(f"Time: {nowFormatted}\nTicked Systems in last Hr = {self.ticked},\nCurrently Tracked Systems = {self.tracked},\nCurrently Observed Systems = {self.observed}")

    def __sendStatusToDiscord(self):
        webhook = DiscordWebhook(url=TEST_DISCORDWEBHOOKURL, content=f'Tracked Systems: {self.tracked}\nTicked Systems: {self.ticked}')
        response = webhook.execute()

