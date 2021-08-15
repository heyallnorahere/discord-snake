import yaml
class Config:
    def __init__(self, config_path: str):
        with open(config_path, "r") as stream:
            data = yaml.load(stream)
        self.snake_head = str(data["snake-head"])
        self.snake_body = str(data["snake-body"])
        self.apple = str(data["apple"])
        self.border = str(data["border"])