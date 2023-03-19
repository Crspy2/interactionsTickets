import asyncio

from interactions import Extension, Client, SlashContext, Embed, \
    Button, ButtonStyle, slash_command
from interactions.api.events import Component

from database.tickets import DBClient


class Open(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @slash_command(
        name="open",
        description="Open a support ticket"
    )
    async def open(self, ctx: SlashContext):
        request = Embed(
            title="🎟️ | Open",
            description='If you want to create a ticket channel for yourself, you have to click to this emoji: `"🎟"` or else click to `"❌"`',
            color=self.client.success
        )
        create = Button(
            style=ButtonStyle.GRAY,
            label="🎟 Create Ticket",
            custom_id="create",
        )
        cancel = Button(
            style=ButtonStyle.GRAY,
            label="❌ Cancel Process",
            custom_id="dont_do",
        )
        too_late = Button(
            style=ButtonStyle.BLUE,
            label="⏰ Time is Up",
            disabled=True
        )
        res = await ctx.send(embed=request, components=[create, cancel], ephemeral=True)
        await asyncio.sleep(60)  # wait for 60 seconds
        await ctx.edit(res, embed=request, components=[too_late])



def setup(client: Client):
    Open(client)