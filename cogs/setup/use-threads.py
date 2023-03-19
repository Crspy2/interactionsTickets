from interactions import Extension, Client, SlashContext, subcommand, slash_option, OptionType, \
    Embed

from database.tickets import DBClient


class Limit(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @subcommand(
        base="setup",
        name="use-threads",
        description="Easily configure the ticket type",
    )
    @slash_option(
        name="use_threads",
        description="Whether or not private threads should be used for tickets",
        required=True,
        opt_type=OptionType.BOOLEAN,
    )
    async def threads(self, ctx: SlashContext):
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

        if ctx.kwargs['use_threads'] and ctx.guild.premium_tier != 2:
            no_perms = Embed(
                title="No Boost",
                description="This server does not have the required server boost tier to have private threads!",
                color=self.client.error
            )
            return await ctx.send(embed=no_perms)

        use_threads = {'use_threads': ctx.kwargs['use_threads']}
        db.update_guild_settings(str(ctx.guild.id), **use_threads)

        confirm_embed = Embed(
            title="Setup",
            description=f"Thread mode has been {'enabled' if ctx.kwargs['use_threads'] else 'disabled'}",
            color=self.client.success
        )
        return await ctx.send(embed=confirm_embed)


def setup(client: Client):
    Limit(client)