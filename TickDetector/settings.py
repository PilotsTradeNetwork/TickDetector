from dotenv import load_dotenv
from os import getenv
load_dotenv()

__Test = True

JOURNAL_SCHEMA_URL      =   getenv("JOURNAL_SCHEMA_URL")
EDDN_RELAY              =   getenv("EDDN_RELAY")
INTERVAL_DURATION_MINS  =   int(getenv("INTERVAL_DURATION_MINS"))
MAX_INTERVALS           =   int(getenv("MAX_INTERVALS"))
MIN_INTERVAL_FREQUENCY  =   int(getenv("MIN_INTERVAL_FREQUENCY"))

# Mode dependent
if __Test == True:
    WEBHOOK_URL         =   getenv("TEST_DISCORDWEBHOOKURL")
else:
    WEBHOOK_URL         =   getenv("PROD_DISCORDWEBHOOKURL")
