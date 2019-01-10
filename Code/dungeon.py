from math import sqrt
from enum import IntEnum
import numpy as np
import random as rand

# A cell of the dungeon
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

# Returns the probability of creationg a certain type of cell during random dungeon creation
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

# The class of the dungeon defined by its size (x, y) and a grid a cells
class Dungeon:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.cells = np.tile(Cell.EMPTY, [x, y])
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self) -> int:
        return 2 * hash(self.x) + 4 * hash(self.y) + 8 * hash(self.name) 

    # Returns true if the position (x, y) is a wall or is outside the dungeon
    def is_wall(self, x, y):
        return x < 0 or x >= self.x or y < 0 or y >= self.y or self.cells[x, y] == Cell.WALL

    # Returns the position of the key
    def getKeyPos(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.cells[i, j] == Cell.KEY:
                    return (i, j)

    # Write the dungeon into a file
    def write(self, fileName):
        file = open(fileName, "w")
        file.write(str(self.x) + " " + str(self.y) + "\n")
        for i in range(self.x):
            for j in range(self.y):
                if self.cells[i, j] == Cell.WALL:
                    file.write("w")
                elif self.cells[i, j] == Cell.TREASURE:
                    file.write("t")
                elif self.cells[i, j] == Cell.START:
                    file.write("o")
                elif self.cells[i, j] == Cell.ENEMY:
                    file.write("e")
                elif self.cells[i, j] == Cell.PORTAL:
                    file.write("p")
                elif self.cells[i, j] == Cell.PLATFORM:
                    file.write("_")
                elif self.cells[i, j] == Cell.CRACKS:
                    file.write("c")
                elif self.cells[i, j] == Cell.TRAP:
                    file.write("r")
                elif self.cells[i, j] == Cell.SWORD:
                    file.write("s")
                elif self.cells[i, j] == Cell.KEY:
                    file.write("k")
                elif self.cells[i, j] == Cell.EMPTY:
                    file.write(" ")
            file.write("\n")
        file.close()

# Create a dungeon based on a dungeon file
def load_dungeon(file):
    with open(file, "r") as file:
        i = 0
        j = 0
        size = file.readline().split(' ')
        dungeon = Dungeon(int(size[0]), int(size[1]), str(file.name))
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

# Create a dungeon at random 
def random_dungeon_generation(x, y):
    d = Dungeon(x, y, "Random")
    # Treasure at top left corner and start at bottom right corner
    d.cells[0, 0] = Cell.TREASURE
    d.cells[x - 1, y - 1] = Cell.START
    # Key and sword in other empty cells
    d.cells[choose_pos(d)] = Cell.KEY
    d.cells[choose_pos(d)] = Cell.SWORD
    # Fill the empty cells
    for i in range(x):
        for j in range(y):
            if d.cells[i, j] == Cell.EMPTY:
                d.cells[i, j] = choose_cell()
    # Test if the dungeon has a solution, if not generates a new one
    if not test_dungeon(d):
        return random_dungeon_generation(x, y)
    return d

# Choose a cell at random given their probability of creation
def choose_cell():
    p = rand.random()
    sump = 0
    for k in list(map(int, Cell)):
        sump += get_creation_proba_cell(k)
        if p <= sump:
            return k
    return Cell.EMPTY

# Choose an empty position of the dungeon
def choose_pos(dungeon):
    x = rand.randint(0, dungeon.x - 1)
    y = rand.randint(0, dungeon.y - 1)
    while dungeon.cells[x, y] != Cell.EMPTY:
        x = rand.randint(0, dungeon.x - 1)
        y = rand.randint(0, dungeon.y - 1)
    return x, y

def isReachable(dungeon, start, target):
    visitedPos = []
    posToTest = []
    posToTest.append(start)
    while len(posToTest) > 0:
        currentPos = posToTest.pop()
        for i, j in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            testingPos = (currentPos[0] + i, currentPos[1] + j)
            # If we already checked the cell, we skip it
            if testingPos in visitedPos:
                continue
            visitedPos.append(testingPos)
            # If it is impossible to pass through the cell (wall or crack), we skip it
            if (dungeon.is_wall(testingPos[0], testingPos[1]) or 
                dungeon.cells[testingPos[0], testingPos[1]] == Cell.CRACKS):
                continue
            # If we've reached the target, we're done
            if (testingPos == target):
                return True
            posToTest.append(testingPos)
    return False


# Test if the dungeon has a solution: there exists a path from every pos to the start and from key to treasure
def test_dungeon(dungeon):
    if dungeon.cells[dungeon.x - 1, dungeon.y - 1] != Cell.START or dungeon.cells[0, 0] != Cell.TREASURE:
        return False
    for i in range(dungeon.x):
        for j in range(dungeon.y):
            if (i, j) != (dungeon.x - 1, dungeon.y - 1):
                if dungeon.cells[i, j] != Cell.WALL and dungeon.cells[i, j] != Cell.CRACKS:
                    if not isReachable(dungeon, (i, j), (dungeon.x - 1, dungeon.y - 1)):
                        return False
    return isReachable(dungeon, dungeon.getKeyPos(), (0, 0)) and isReachable(dungeon, (0, 0), dungeon.getKeyPos())