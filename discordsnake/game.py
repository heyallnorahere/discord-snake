import discordsnake.util as util
import random
class Game:
    def __init__(self, width: int, height: int):
        random.seed()
        self.width = width
        self.height = height
        self.snake_position = util.generate_position(self.width, self.height)
        self.snake_body_positions = list[tuple[int, int]]()
        self.apple_position = (0, 0)
        self.generate_apple_position()
        self.game_running = True
    def update(self, snake_movement: tuple[int, int]):
        new_position = util.add_vectors(self.snake_position, snake_movement)
        if new_position == self.apple_position:
            self.snake_body_positions.append(self.snake_position)
            self.snake_position = new_position
            self.generate_apple_position()
        else:
                
            body_position_count = len(self.snake_body_positions)
            for i in range(body_position_count):
                if i >= body_position_count - 1:
                    new_body_position = self.snake_position
                else:
                    new_body_position = self.snake_body_positions[i + 1]
                self.snake_body_positions[i] = new_body_position
            self.snake_position = new_position
            if self.is_snake_out_of_bounds():
                if self.snake_position[0] < 0:
                    self.snake_position[0] = self.width - 1
                elif self.snake_position[0] >= self.width:
                    self.snake_position[0] = 0
                if self.snake_position[1] < 0:
                    self.snake_position[1] = self.height - 1
                elif self.snake_position[1] >= self.height:
                    self.snake_position[1] = 0
            if self.snake_position in self.snake_body_positions:
                self.game_running = False
    def generate_apple_position(self):
        positions = self.snake_body_positions.copy()
        positions.append(self.snake_position)
        done = False
        while not done:
            self.apple_position = util.generate_position(self.width, self.height)
            if not self.apple_position in positions:
                done = True
    def is_snake_out_of_bounds(self):
        if self.snake_position[0] < 0:
            return True
        if self.snake_position[0] >= self.width:
            return True
        if self.snake_position[1] < 0:
            return True
        if self.snake_position[1] >= self.height:
            return True
        return False