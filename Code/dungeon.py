from math import sqrt
from enum import IntEnum
import numpy as np
import random as rand

class Cell(IntEnum):
    START = 1
    EMPTY = 2
    WALL = 3
    ENEMY = 4
    TRAP = 5
    CRACKS = 6
    TREASURE = 7
    SWORD = 8
    KEY = 9
    PORTAL = 10
    PLATFORM = 11

def get_creation_proba_cell(c):
    if c == Cell.EMPTY:
        return 0.4
    elif c == Cell.WALL:
        return 0.2
    elif c == Cell.ENEMY:
        return 0.1
    elif c == Cell.TRAP:
        return 0.1
    elif c == Cell.CRACKS:
        return 0.05
    elif c == Cell.PORTAL:
        return 0.05
    elif c == Cell.PLATFORM:
        return 0.1
    else:
        return 0

class Dungeon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cells = np.tile(Cell.EMPTY, [x, y])

    def is_wall(self, x, y):
        return x < 0 or x >= self.x or y < 0 or y >= self.y or self.cells[x, y] == Cell.WALL

    def find_key(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.cells[i, j] == Cell.KEY:
                    return i, j
        return None

def load_dungeon(file):
    with open(file, "r") as file:
        i = 0
        j = 0
        size = file.readline().split(' ')
        dungeon = Dungeon(int(size[0]), int(size[1]))
        for ligne in file.readlines():
            for c in ligne:
                if c == 'w':
                    dungeon.cells[i, j] = Cell.WALL
                elif c == 't':
                    dungeon.cells[i, j] = Cell.TREASURE
                elif c == 'o':
                    dungeon.cells[i, j] = Cell.START
                elif c == 'e':
                    dungeon.cells[i, j] = Cell.ENEMY
                elif c == 'p':
                    dungeon.cells[i, j] = Cell.PORTAL
                elif c == '_':
                    dungeon.cells[i, j] = Cell.PLATFORM
                elif c == 'c':
                    dungeon.cells[i, j] = Cell.CRACKS
                elif c == 'r':
                    dungeon.cells[i, j] = Cell.TRAP
                elif c == 's':
                    dungeon.cells[i, j] = Cell.SWORD
                elif c == 'k':
                    dungeon.cells[i, j] = Cell.KEY
                i += 1
            i = 0
            j += 1
        return dungeon

def random_dungeon_generation(x, y):
    d = Dungeon(x, y)
    d.cells[0, 0] = Cell.TREASURE
    d.cells[x - 1, y - 1] = Cell.START
    d.cells[choose_pos(d)] = Cell.KEY
    d.cells[choose_pos(d)] = Cell.SWORD
    for i in range(x):
        for j in range(y):
            if d.cells[i, j] != Cell.EMPTY:
                continue
            d.cells[i, j] = choose_cell()
    if not test_dungeon(d):
        return random_dungeon_generation(x, y)
    return d

def choose_cell():
    p = rand.random()
    sump = 0
    for k in list(map(int, Cell)):
        sump += get_creation_proba_cell(k)
        if p <= sump:
            return k
    return Cell.EMPTY

def choose_pos(dungeon):
    x = rand.randint(0, dungeon.x - 1)
    y = rand.randint(0, dungeon.y - 1)
    while dungeon.cells[x, y] != Cell.EMPTY:
        x = rand.randint(0, dungeon.x - 1)
        y = rand.randint(0, dungeon.y - 1)
    return x, y

def test_dungeon(dungeon):
    if dungeon.cells[dungeon.x - 1, dungeon.y - 1] != Cell.START or dungeon.cells[0, 0] != Cell.TREASURE:
        return False
    points_ok = [(0, 0)]
    points = [(0, 0)]
    access_start = False
    access_key = False
    while len(points_ok) > 0 and (not access_key or not access_start):
        point = points_ok.pop()
        for i, j in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            point_test = (point[0] + i, point[1] + j)
            if point_test in points:
                continue
            points.append(point_test)
            if dungeon.is_wall(point_test[0], point_test[1]) or dungeon.cells[point_test[0], point_test[1]] == Cell.CRACKS:
                continue
            if dungeon.cells[point_test] == Cell.KEY:
                access_key = True
            if dungeon.cells[point_test] == Cell.START:
                access_start = True
            points_ok.append(point_test)
    return access_start and access_key