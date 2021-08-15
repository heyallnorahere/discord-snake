import discord
from discordsnake.config import Config
from discordsnake.game import Game
BORDER = 0
SNAKE_HEAD = 1
SNAKE_BODY = 2
APPLE = 3
BLANK = 4
NEWLINE_CHARACTER = 5
class DiscordGame:
    def __init__(self, message: discord.Message, config: Config):
        self.message = message
        self.config = config
        game_size = self.config.game_size
        self.game = Game(game_size[0], game_size[1])
    async def update_message(self):
        character_translation_table = {
            BORDER: self.config.border,
            SNAKE_HEAD: self.config.snake_head,
            SNAKE_BODY: self.config.snake_body,
            APPLE: self.config.apple,
            BLANK: self.config.blank_tile,
            NEWLINE_CHARACTER: "\n"
        }
        characters = list[int]()
        game_size = self.config.game_size
        for _ in range(game_size[0] + 2):
            characters.append(BORDER)
        characters.append(NEWLINE_CHARACTER)
        for y in range(game_size[1]):
            characters.append(BORDER)
            for x in range(game_size[0]):
                position = (x, y)
                if position == self.game.apple_position:
                    characters.append(APPLE)
                elif position == self.game.snake_position:
                    characters.append(SNAKE_HEAD)
                elif position in self.game.snake_body_positions:
                    characters.append(SNAKE_BODY)
                else:
                    characters.append(BLANK)
            characters.append(BORDER)
            characters.append(NEWLINE_CHARACTER)
        for _ in range(game_size[0] + 2):
            characters.append(BORDER)
        content = ""
        for key in characters:
            content += character_translation_table[key]
        embed = self.message.embeds[0]
        embed.description = content
        await self.message.edit(embed=embed)
class SnakeClient(discord.Client):
    def __init__(self, config: Config):
        self.config = config
        self.games = dict[str, DiscordGame]()
        super().__init__()
    async def on_ready(self):
        print(f"successfully connected as {self.user}")
    async def on_message(self, message: discord.Message):
        if message.content.__class__ == str:
            content = str(message.content)
            prefix = self.config.command_prefix
            if content.startswith(prefix):
                index = content.find(prefix)
                command = content[(index + len(prefix)):]
                commands = {
                    "start": self.start_game
                }
                try:
                    await commands[command](message.channel, message.author.display_name)
                except KeyError:
                    await message.channel.send("Could not execute the specified command!")
    async def start_game(self, channel: discord.TextChannel, user_name: str):
        embed = discord.Embed(title=f"Snake game: {user_name}")
        message = await channel.send(embed=embed)
        game = DiscordGame(message, self.config)
        await game.update_message()
        self.games[user_name] = game