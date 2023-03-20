import os
from interactions import Client, Intents
from dotenv import load_dotenv

from handlers import events, commands

load_dotenv()

client = Client(
    token=os.environ.get("TOKEN"),
    intents=Intents.DEFAULT,
    debug_scope=1086848383488106536,
    disable_dm_commands=True,

    send_command_tracebacks=True,
    show_ratelimit_tracebacks=True,

    basic_logging=True,
)

#  Bot-Wide Variables
client.db_uri = os.environ.get("MONGO_URI")
client.success = 0x65C97A
client.error = 0xE85041

commands.load(client)
events.load(client)

client.start()
