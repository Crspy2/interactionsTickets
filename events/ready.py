from interactions import listen, Client, Extension


class OnReady(Extension):
    def __init__(self, client: Client):
        self.bot: Client = client

    @listen()
    async def on_ready(self):
        print(f"Connected to tickets as {self.client.user.username}#{self.client.user.discriminator}")


def setup(client: Client):
    OnReady(client)