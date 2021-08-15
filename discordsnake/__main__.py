from discordsnake import *
with open("token.txt", "r") as stream:
    token = stream.read()
config = Config("config.yml")
client = SnakeClient(config)
client.run(token)