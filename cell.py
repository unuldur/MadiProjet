from enum import Enum
from etat import Etat


class Cell(Enum):
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


proba_cell = dict()
proba_cell[Cell.EMPTY] = 0.4
proba_cell[Cell.WALL] = 0.2
proba_cell[Cell.ENEMY] = 0.1
proba_cell[Cell.TRAP] = 0.1
proba_cell[Cell.CRACKS] = 0.05
proba_cell[Cell.PORTAL] = 0.05
proba_cell[Cell.PLATFORM] = 0.1


def cell_movement(cell, dungeon, state):
    if cell == Cell.EMPTY:
        return [(1, Etat.STAY)]
    if cell == Cell.START:
        return [(1, Etat.WIN)] if state.treasure else [(1, Etat.STAY)]
    if cell == Cell.KEY:
        return [(1, Etat.GET_KEY)] if not state.key else [(1, Etat.STAY)]
    if cell == Cell.SWORD:
        return [(1, Etat.GET_SWORD)] if not state.sword else [(1, Etat.STAY)]
    if cell == Cell.TREASURE:
        return [(1, Etat.GET_TREASURE)] if state.key and not state.treasure else [(1, Etat.STAY)]
    if cell == Cell.CRACKS:
        return [(1, Etat.DEAD)]
    if cell == Cell.ENEMY:
        return [(0.7, Etat.KILL_ENEMY), (0.3, Etat.DEAD)] if not state.sword else [(1, Etat.KILL_ENEMY)]
    if cell == Cell.TRAP:
        return [(0.1, Etat.DEAD), (0.3, Etat.MOVE, (dungeon.x - 1, dungeon.y - 1)), (0.6, Etat.STAY)]
    if cell == Cell.PLATFORM:
        nb_wall = 0
        possible_cell = []
        for (i, j) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if not dungeon.is_wall(state.pos[0] + i, state.pos[1] + j):
                nb_wall += 1
                possible_cell.append((state.pos[0] + i, state.pos[1] + j))
        res = []
        for c in possible_cell:
            res.append((1 / nb_wall, Etat.MOVE, c))
        return res
    if cell == Cell.PORTAL:
        nb = 0
        possible_cell = []
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j) and i != state.pos[0] and j != state.pos[1]:
                    nb += 1
                    possible_cell.append((i, j))
        res = []
        for c in possible_cell:
            res.append((1 / nb, Etat.MOVE, c))
        return res
    return []

