from dotenv import load_dotenv
from os import getenv
load_dotenv()

__Test = True

JOURNAL_SCHEMA_URL  =   getenv("JOURNAL_SCHEMA_URL")
EDDN_RELAY          =   getenv("EDDN_RELAY")

# Mode dependent
if __Test == True:
    WEBHOOK_URL     =   getenv("TEST_DISCORDWEBHOOKURL")
else:
    WEBHOOK_URL     =   getenv("PROD_DISCORDWEBHOOKURL")
