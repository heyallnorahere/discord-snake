import discord
from discordsnake.config import Config
from discordsnake.game import Game
class DiscordGame:
    BORDER = 0
    SNAKE_HEAD = 1
    SNAKE_BODY = 2
    APPLE = 3
    BLANK = 4
    NEWLINE_CHARACTER = 5
    def __init__(self, message: discord.Message, config: Config):
        self.message = message
        self.config = config
        game_size = self.config.game_size
        self.game = Game(game_size[0], game_size[1])
    async def update_message(self):
        character_translation_table = {
            DiscordGame.BORDER: self.config.border,
            DiscordGame.SNAKE_HEAD: self.config.snake_head,
            DiscordGame.SNAKE_BODY: self.config.snake_body,
            DiscordGame.APPLE: self.config.apple,
            DiscordGame.BLANK: self.config.blank_tile,
            DiscordGame.NEWLINE_CHARACTER: "\n"
        }
        characters = list[int]()
        game_size = self.config.game_size
        for _ in range(game_size[0] + 2):
            characters.append(DiscordGame.BORDER)
        characters.append(DiscordGame.NEWLINE_CHARACTER)
        for y in range(game_size[1]):
            characters.append(DiscordGame.BORDER)
            for x in range(game_size[0]):
                position = (x, y)
                if position == self.game.apple_position:
                    characters.append(DiscordGame.APPLE)
                elif position == self.game.snake_position:
                    characters.append(DiscordGame.SNAKE_HEAD)
                elif position in self.game.snake_body_positions:
                    characters.append(DiscordGame.SNAKE_BODY)
                else:
                    characters.append(DiscordGame.BLANK)
            characters.append(DiscordGame.BORDER)
            characters.append(DiscordGame.NEWLINE_CHARACTER)
        for _ in range(game_size[0] + 2):
            characters.append(DiscordGame.BORDER)
        content = ""
        for key in characters:
            content += character_translation_table[key]
        embed = self.message.embeds[0]
        embed.description = content
        await self.message.edit(embed=embed)
class SnakeClient(discord.Client):
    ARROWS = [
        "⬆️",
        "⬇",
        "⬅️",
        "➡️"
    ]
    def __init__(self, config: Config):
        self.config = config
        self.games = dict[str, DiscordGame]()
        super().__init__()
    async def on_ready(self):
        print(f"the snake bot is now online as {self.user}")
    async def on_message(self, message: discord.Message):
        if message.content.__class__ == str:
            content = str(message.content)
            prefix = self.config.command_prefix
            if content.startswith(prefix):
                index = content.find(prefix)
                command = content[(index + len(prefix)):]
                commands = {
                    "start": self.start_game,
                    "stop": self.stop_game,
                    "help": self.print_help
                }
                try:
                    await commands[command](message.channel, message.author.display_name)
                except KeyError:
                    await message.channel.send("Could not execute the specified command!")
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        for user_name in self.games.keys():
            await self.update_game_message(user_name)
        if not payload.emoji.name in SnakeClient.ARROWS:
            return
        arrow_translation_table = {
            SnakeClient.ARROWS[0]: (0, -1),
            SnakeClient.ARROWS[1]: (0, 1),
            SnakeClient.ARROWS[2]: (-1, 0),
            SnakeClient.ARROWS[3]: (1, 0)
        }
        for user_name in self.games.keys():
            game = self.games[user_name]
            message = game.message
            if message.id == payload.message_id:
                if user_name == payload.member.display_name:
                    game.game.update(arrow_translation_table[payload.emoji.name])
                    await game.update_message()
                    self.games[user_name] = game
                    await message.remove_reaction(payload.emoji, payload.member)
                    if not game.game.game_running:
                        await message.channel.send(f"Game over, <@{payload.user_id}>!")
                        self.games.pop(user_name)
                        break
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        for user_name in self.games.keys():
            await self.update_game_message(user_name)
    async def start_game(self, channel: discord.TextChannel, user_name: str):
        embed = discord.Embed(title=f"Snake game: {user_name}")
        message = await channel.send(embed=embed)
        game = DiscordGame(message, self.config)
        await game.update_message()
        for arrow in SnakeClient.ARROWS:
            await game.message.add_reaction(discord.PartialEmoji(name=arrow))
        self.games[user_name] = game
        await self.update_game_message(user_name)
    async def stop_game(self, channel: discord.TextChannel, user_name: str):
        try:
            self.games.pop(user_name)
            await channel.send(f"Terminated **{user_name}**'s snake game.")
        except KeyError:
            await channel.send(f"**{user_name}**, you are not currently playing a game of snake!")
    async def print_help(self, channel: discord.TextChannel, user_name: str):
        command_prefix = self.config.command_prefix
        await channel.send(f"To use this bot,\nSay `{command_prefix}start` to start a game,\nand `{command_prefix}stop` to stop it.")
    async def update_game_message(self, user_name: str):
        game = self.games[user_name]
        message = game.message
        channel: discord.TextChannel = self.get_channel(message.channel.id)
        message = await channel.fetch_message(message.id)
        game.message = message
        self.games[user_name]