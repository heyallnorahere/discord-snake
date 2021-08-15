import random
def add_vectors(v1: tuple[int, int], v2: tuple[int, int]):
    return (v1[0] + v2[0], v1[1] + v2[1])
def invert_vector(vector: tuple[int, int]):
    return (-vector[0], -vector[1])
def sub_vectors(v1: tuple[int, int], v2: tuple[int, int]):
    return add_vectors(v1, invert_vector(v2))
def generate_position(board_width: int, board_height: int):
    x = random.randrange(board_width)
    y = random.randrange(board_height)
    return (x, y)