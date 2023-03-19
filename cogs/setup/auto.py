import interactions
from interactions import Extension, Client, SlashContext, subcommand, PermissionOverwrite, \
    Embed, OverwriteType, Permissions

from database.tickets import DBClient


class Auto(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @subcommand(
        base="setup",
        name="auto",
        description="Easily configure the ticket system",
    )
    async def auto(self, ctx: SlashContext):
        await ctx.defer(ephemeral=True)
        db = DBClient(self.client.db_uri)
        settings = db.get_guild_settings(str(ctx.guild.id))
        admins = settings['admins']
        support = settings['support']

        author_roles = []
        for role in ctx.author.roles:
            author_roles.append(str(role.id))

        has_admin_roles = set(author_roles).intersection(set(settings['admins']))

        # Check if interaction author is an admin
        if not db.is_user_admin(str(ctx.guild.id), str(ctx.author.user.id)):
            if not has_admin_roles:
                no_perms = Embed(
                    title="Error",
                    description="You do not have permissions for this command!",
                    color=self.client.error
                )
                return await ctx.send(embed=no_perms)

        admin_role = await ctx.guild.create_role("Tickets Admin", hoist=True)
        support_role = await ctx.guild.create_role("Tickets Support", hoist=True)

        transcript_channel = await ctx.guild.create_text_channel(
            name="transcripts",
            topic="The channel where ticket transcripts are sent",
            permission_overwrites=[
                PermissionOverwrite(
                    id=ctx.guild.default_role.id,
                    type=OverwriteType(value="role"),
                    deny=Permissions.VIEW_CHANNEL.SEND_MESSAGES
                ),
                PermissionOverwrite(
                    id=admin_role.id,
                    type=OverwriteType(value="role"),
                    allow=Permissions.VIEW_CHANNEL,
                    deny=Permissions.SEND_MESSAGES
                ),
                PermissionOverwrite(
                    id=support_role.id,
                    type=OverwriteType(value="role"),
                    allow=Permissions.VIEW_CHANNEL,
                    deny=Permissions.SEND_MESSAGES
                ),
            ]
        )

        tickets_category = await ctx.guild.create_category("Tickets")
        admins.append(str(admin_role.id))
        support.append(str(support_role.id))

        new_support = {'support': support}
        new_admin = {'admins': admins}
        new_category = {'default_category': tickets_category.id}
        new_transcript_channel = {'transcript_channel': transcript_channel.id}

        db.update_guild_settings(str(ctx.guild.id), **new_admin, **new_support, **new_category, **new_transcript_channel)

        confirm_embed = Embed(
            title="Setup",
            description=f"<:enable1:1086878041894035589><:enable2:1086878042959396866> Created `{admin_role.name}` and `{support_role.name}` roles\n"
                        f"<:enable1:1086878041894035589><:enable2:1086878042959396866> {transcript_channel.mention} channel \n"
                        "<:enable1:1086878041894035589><:enable2:1086878042959396866> Created Tickets Category\n"
                        "\n"
                        "Setup complete. The `Tickets Admin` and `Tickets Support` roles have been added to the the default panel!",
            color=self.client.success
        )
        return await ctx.send(embed=confirm_embed)


def setup(client: Client):
    Auto(client)