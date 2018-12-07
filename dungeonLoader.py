from cell import *
from dungeon import Dungeon
import random as rand

def load_dungeon(file):
    with open(file, "r") as file:
        i = 0
        j = 0
        size = file.readline().split(' ')
        dungeon = Dungeon(int(size[0]), int(size[1]))
        for ligne in file.readlines():
            for c in ligne:
                if c == 'w':
                    dungeon.dungeon[i, j] = Cell.WALL
                elif c == 't':
                    dungeon.dungeon[i, j] = Cell.TREASURE
                elif c == 'o':
                    dungeon.dungeon[i, j] = Cell.START
                elif c == 'e':
                    dungeon.dungeon[i, j] = Cell.ENEMY
                elif c == 'p':
                    dungeon.dungeon[i, j] = Cell.PORTAL
                elif c == '_':
                    dungeon.dungeon[i, j] = Cell.PLATFORM
                elif c == 'c':
                    dungeon.dungeon[i, j] = Cell.CRACKS
                elif c == 'r':
                    dungeon.dungeon[i, j] = Cell.TRAP
                elif c == 's':
                    dungeon.dungeon[i, j] = Cell.SWORD
                elif c == 'k':
                    dungeon.dungeon[i, j] = Cell.KEY
                i += 1
            i = 0
            j += 1
        return dungeon


def random_dungeon_generation(x, y):
    d = Dungeon(x, y)
    d.dungeon[0, 0] = Cell.TREASURE
    d.dungeon[x - 1, y - 1] = Cell.START
    d.dungeon[choose_pos(d)] = Cell.KEY
    d.dungeon[choose_pos(d)] = Cell.SWORD
    for i in range(x):
        for j in range(y):
            if d.dungeon[i, j] != Cell.EMPTY:
                continue
            d.dungeon[i, j] = choose_cell()
    if not test_dungeon(d):
        return random_dungeon_generation(x, y)
    return d


def choose_cell():
    p = rand.random()
    sump = 0
    for k in proba_cell.keys():
        sump += proba_cell[k]
        if p <= sump:
            return k
    return Cell.EMPTY


def choose_pos(dungeon):
    x = rand.randint(0, dungeon.x - 1)
    y = rand.randint(0, dungeon.y - 1)
    while dungeon.dungeon[x, y] != Cell.EMPTY:
        x = rand.randint(0, dungeon.x - 1)
        y = rand.randint(0, dungeon.y - 1)
    return x, y


def test_dungeon(dungeon):
    if dungeon.dungeon[dungeon.x - 1, dungeon.y - 1] != Cell.START or dungeon.dungeon[0, 0] != Cell.TREASURE:
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
            if dungeon.is_wall(point_test[0], point_test[1]) or dungeon.dungeon[point_test[0], point_test[1]] == Cell.CRACKS:
                continue
            if dungeon.dungeon[point_test] == Cell.KEY:
                access_key = True
            if dungeon.dungeon[point_test] == Cell.START:
                access_start = True
            points_ok.append(point_test)
    return access_start and access_key