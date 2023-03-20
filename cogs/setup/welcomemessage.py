from interactions import Extension, Client, SlashContext, subcommand, Embed, Modal, ParagraphText, ModalContext, \
    ShortText

from database.tickets import DBClient


class TextInput:
    pass


class WelcomeMessage(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @subcommand(
        base="setup",
        name="welcomemessage",
        description="Easily configure the default ticket welcome message",
    )
    async def welcome_message(self, ctx: SlashContext):
        welcome_modal = Modal(
            ParagraphText(
                label="Welcome Message",
                placeholder="Thank you for contacting support! Please wait for a support member to assist you!",
                custom_id="welcome_message"
            ),
            title="My Modal",
        )
        await ctx.send_modal(modal=welcome_modal)

        welcome_modal_ctx: ModalContext = await ctx.bot.wait_for_modal(welcome_modal)

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
                return await welcome_modal_ctx.send(embed=no_perms)

        new_message = {'welcome_message': rf"{welcome_modal_ctx.responses['welcome_message']}"}
        db.update_guild_settings(str(ctx.guild.id), **new_message)

        confirm_embed = Embed(
            title="Setup",
            description="The welcome message has been updated. Open a ticket to see it in action",
            color=self.client.success
        )
        await welcome_modal_ctx.send(embed=confirm_embed)


def setup(client: Client):
    WelcomeMessage(client)
