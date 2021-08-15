import discord
from discordsnake.config import Config
class SnakeClient(discord.Client):
    def __init__(self, config: Config):
        self.config = config
        super().__init__()
    async def on_ready(self):
        print(f"successfully connected as {self.user}")
    async def on_message(self, message: discord.Message):
        print(f"message from {message.author}: {message.content}")