from interactions import listen, Client, Extension
from interactions.api.events import RoleDelete

from database.tickets import DBClient


class OnRoleDelete(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @listen()
    async def on_role_delete(self, event: RoleDelete):
        db = DBClient(self.client.db_uri)
        settings = db.get_guild_settings(str(event.guild.id))
        admins = settings['admins']
        support = settings['support']

        if db.is_user_admin(str(event.guild.id), str(event.role.id)):
            admins.remove(str(event.role.id))
            old_admin = {'admins': admins}

            db.update_guild_settings(str(event.guild.id), **old_admin)

        if db.is_user_support(str(event.guild.id), str(event.role.id)):
            support.remove(str(event.role.id))
            old_support = {'support': support}

            db.update_guild_settings(str(event.guild.id), **old_support)


def setup(client: Client):
    OnRoleDelete(client)