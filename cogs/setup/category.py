from interactions import Extension, Client, SlashContext, subcommand, slash_option, OptionType, \
    Embed

from database.tickets import DBClient


class Category(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @subcommand(
        base="setup",
        name="category",
        description="Easily configure the default ticket category",
    )
    @slash_option(
        name="category",
        description="The name of the channel category",
        required=True,
        opt_type=OptionType.MENTIONABLE,
    )
    async def category(self, ctx: SlashContext, limit: int):
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

        ticket_limit = {'ticket_limit': limit}
        db.update_guild_settings(str(ctx.guild.id), **ticket_limit)

        confirm_embed = Embed(
            title="Setup",
            description=f"The ticket limit has been updated to `{limit}",
            color=self.client.success
        )
        return await ctx.send(embed=confirm_embed)


def setup(client: Client):
    Category(client)