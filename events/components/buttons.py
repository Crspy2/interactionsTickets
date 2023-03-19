import interactions
from interactions import listen, Button, Client, Extension, Embed, ButtonStyle
from interactions.api.events import Component

from database.tickets import DBClient


class Buttons(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @listen()
    async def on_component(self, event: Component):
        db = DBClient(self.client.db_uri)
        settings = db.get_guild_settings(str(event.ctx.guild.id))
        admins = settings['admins']
        support = settings['support']

        custom_id = event.ctx.custom_id
        if custom_id.startswith("addadmin_"):
            new_admin_id = custom_id.split("_")[1]
            # Check if user is OWNER
            owner = await event.ctx.guild.fetch_owner()
            if new_admin_id == owner.id:
                is_owner = Embed(
                    title="Error",
                    description="The server owner must be an admin",
                    color=self.client.error
                )
                return await event.ctx.edit_origin(embed=is_owner, components=[])

            # Check if user is already an admin:
            if db.is_user_admin(str(event.ctx.guild.id), str(new_admin_id)):
                error_embed = Embed(
                    title="Error",
                    description="User is already an admin!",
                    color=self.client.error
                )
                return await event.ctx.edit_origin(embed=error_embed, components=[])

            # Check if user is a support representative
            if db.is_user_support(str(event.ctx.guild.id), str(new_admin_id)):
                support = support
                support.remove(str(new_admin_id))
                new_support = {'support': support}
                db.update_guild_settings(str(event.ctx.guild.id), **new_support)

            admins.append(new_admin_id)
            new_admins = {'admins': admins}

            db.update_guild_settings(str(event.ctx.guild.id), **new_admins)

            # Tell user how it went!
            confirm_embed = Embed(
                title="Add Admin",
                description=f"Admin added successfully",
                color=self.client.success
            )
            return await event.ctx.edit_origin(embed=confirm_embed, components=[])
        elif custom_id.startswith("addsupport_"):
            new_support_id = custom_id.split("_")[1]
            # Check if user is OWNER
            owner = await event.ctx.guild.fetch_owner()
            if new_support_id == owner.id:
                is_owner = Embed(
                    title="Error",
                    description="The server owner is already an administrator",
                    color=self.client.error
                )
                return await event.ctx.edit_origin(embed=is_owner, components=[])

            # Check if user is already an admin:
            if db.is_user_admin(str(event.ctx.guild.id), str(new_support_id)):
                error_embed = Embed(
                    title="Error",
                    description="User is already an admin!",
                    color=self.client.error
                )
                return await event.ctx.edit_origin(embed=error_embed, components=[])

            # Check if user is already on the support team:
            if db.is_user_support(str(event.ctx.guild.id), str(new_support_id)):
                error_embed = Embed(
                    title="Error",
                    description="User is already a support representative!",
                    color=self.client.error
                )
                return await event.ctx.edit_origin(embed=error_embed, components=[])

            support.append(new_support_id)
            new_support = {'support': support}

            db.update_guild_settings(str(event.ctx.guild.id), **new_support)

            # Tell user how it went!
            confirm_embed = Embed(
                title="Add Support",
                description=f"Support representative added successfully",
                color=self.client.success
            )
            return await event.ctx.edit_origin(embed=confirm_embed, components=[])
        elif custom_id == "create":
            if db.get_ticket(str(event.ctx.guild.id), str(event.ctx.author_id)) is not None:
                if len(db.get_ticket(str(event.ctx.guild.id), str(event.ctx.author_id))) > settings['ticket_limit']:
                    await event.ctx.edit_origin(
                        embed=Embed(
                            title="Error",
                            description="You already have reached the max number of simultaneous open tickets allowed per user!"
                        )
                    )
                if not settings['panels']:
                    return event.ctx.edit_origin(
                        embed=Embed(
                            description="🎫 | Hello, please select option to create a ticket channel from the menu below.",
                            color=self.client.success
                        )
                    )
                else:
                    return event.ctx.edit_origin(
                        embed=Embed(
                            description="🎫 | Hello, please select some option for your ticket reason from the menu below.'",
                            color=self.client.success)
                        )
        elif custom_id == "dont_do" or "cancel":
            await event.ctx.edit_origin(
                embed=Embed(
                    title="Cancelled",
                    description="You have canceled your request to work some thing and now the work have bin canceled for you. Good luck and victory.",
                    color=self.client.error,
                ),
                components=[
                    Button(
                        style=ButtonStyle.RED,
                        label="Cancelled",
                        custom_id="dont_close",
                        emoji=":x:",
                        disabled=True
                    )
                ]
            )


def setup(client: Client):
    Buttons(client)