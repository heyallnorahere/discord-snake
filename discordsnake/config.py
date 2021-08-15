import yaml
class Config:
    def __init__(self, config_path: str):
        with open(config_path, "r") as stream:
            data = yaml.load(stream, Loader=yaml.Loader)
        self.snake_head = str(data["snake-head"])
        self.snake_body = str(data["snake-body"])
        self.apple = str(data["apple"])
        self.border = str(data["border"])
        self.blank_tile = str(data["blank"])
        self.game_size = tuple[int, int](data["game-size"])
        try:
            self.command_prefix = str(data["command-prefix"])
        except KeyError:
            self.command_prefix = "!"