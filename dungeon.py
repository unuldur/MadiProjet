from math import sqrt

import numpy as np

from cell import Cell


class Dungeon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dungeon = np.tile(Cell.EMPTY, [x, y])

    def is_wall(self, x, y):
        return x < 0 or x >= self.x or y < 0 or y >= self.y or self.dungeon[x, y] == Cell.WALL

    def dist_start_key(self):
        x, y = self.find_key()
        x2 = self.x - 1
        y2 = self. y - 1
        return self.dist((x, y), (x2, y2))

    def dist_key_treasure(self):
        x, y = self.find_key()
        return self.dist((x, y), (0, 0))

    def dist_start_treasure(self):
        return self.dist((self.x - 1, self.y - 1), (0, 0))

    def dist(self, pos, pos2):
        return sqrt((pos[0] - pos2[0]) * (pos[0] - pos2[0]) + (pos[1] - pos2[1]) * (pos[1] - pos2[1]))

    def find_key(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.dungeon[i, j] == Cell.KEY:
                    return i, j
        return None
