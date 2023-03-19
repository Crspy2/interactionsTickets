import asyncio

from interactions import listen, Client, Extension
from interactions.api.events import GuildLeft

from database.tickets import DBClient


class GuildLeave(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @listen()
    async def on_guild_left(self, event: GuildLeft):
        await asyncio.sleep(1296000)
        db = DBClient(self.client.db_client)
        db.delete_guild(str(event.guild.id))


def setup(client: Client):
    GuildLeave(client)