from cell import Cell
from dungeon import Dungeon


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

