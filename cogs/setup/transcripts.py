from interactions import Extension, Client, SlashContext, subcommand, slash_option, OptionType, \
    GuildChannel, Embed

from database.tickets import DBClient


class Transcripts(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @subcommand(
        base="setup",
        name="transcripts",
        description="Easily configure the ticket transcripts settings",
    )
    @slash_option(
        name="channel",
        description="The channel that ticket transcripts should be sent to",
        required=True,
        opt_type=OptionType.CHANNEL
    )
    async def transcripts(self, ctx: SlashContext, channel: GuildChannel):
        await ctx.defer(ephemeral=True)
        db = DBClient(self.client.db_uri)
        settings = db.get_guild_settings(str(ctx.guild.id))

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

        transcript_id = {'transcript_channel': channel.id}
        db.update_guild_settings(str(ctx.guild.id), **transcript_id)

        confirm_embed = Embed(
            title="Setup",
            description=f"The transcripts channel has been changed to {channel.mention}",
            color=self.client.success
        )
        return await ctx.send(embed=confirm_embed)


def setup(client: Client):
    Transcripts(client)