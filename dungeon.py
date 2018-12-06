import numpy as np

from cell import Cell


class Dungeon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dungeon = np.tile(Cell.EMPTY, [x, y])

    def is_wall(self, x, y):
        return x < 0 or x >= self.x or y < 0 or y >= self.y or self.dungeon[x, y] == Cell.WALL
