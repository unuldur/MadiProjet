from enum import IntEnum, Enum
import random as rand

from dungeon import Cell
from state import State

class GameState(IntEnum):
    WIN = 0
    DEAD = 1
    FINISH = 3
    NONE = 2

class Movement(Enum):
    LEFT = (1, 0)
    RIGHT = (-1, 0)
    TOP = (0, -1)
    DOWN = (0, 1)
    STOP = ()

class PlayerState(IntEnum):
    MOVE = 1
    DEAD = 2
    STAY = 3
    GET_KEY = 4
    GET_SWORD = 5
    GET_TREASURE = 7
    WIN = 6
    KILL_ENEMY = 8

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.key = False
        self.sword = False
        self.treasure = False

    def go_left(self, dungeon):
        if dungeon.is_wall(self.x - 1, self.y):
            return
        self.x -= 1

    def go_right(self, dungeon):
        if dungeon.is_wall(self.x + 1, self.y):
            return
        self.x += 1

    def go_up(self, dungeon):
        if dungeon.is_wall(self.x, self.y - 1):
            return
        self.y -= 1

    def go_down(self, dungeon):
        if dungeon.is_wall(self.x, self.y + 1):
            return
        self.y += 1

    def set_new_pos(self, x, y):
        self.x = x
        self.y = y

    def get_state(self):
        return State(self.treasure, self.key, self.sword, (self.x, self.y))

    def do_move(self, input_method, dungeon):
        next_cell = get_next_player_state(dungeon.cells[self.x, self.y], dungeon, self.get_state())
        next_move = self.do_action(next_cell)
        if next_move[1] == PlayerState.MOVE:
            self.x = next_move[2][0]
            self.y = next_move[2][1]
            return GameState.NONE
        if next_move[1] == PlayerState.WIN:
            return GameState.WIN
        if next_move[1] == PlayerState.DEAD:
            return GameState.DEAD
        if next_move[1] == PlayerState.GET_TREASURE:
            self.treasure = True
            dungeon.cells[self.x, self.y] = Cell.EMPTY
        if next_move[1] == PlayerState.GET_SWORD:
            self.sword = True
            dungeon.cells[self.x, self.y] = Cell.EMPTY
        if next_move[1] == PlayerState.GET_KEY:
            self.key = True
            dungeon.cells[self.x, self.y] = Cell.EMPTY
        if next_move[1] == PlayerState.KILL_ENEMY:
            dungeon.cells[self.x, self.y] = Cell.EMPTY
        move = input_method.get_next_move(self.get_state())
        if move == Movement.STOP:
            return GameState.FINISH
        if move == Movement.DOWN:
            self.go_down(dungeon)
        if move == Movement.TOP:
            self.go_up(dungeon)
        if move == Movement.LEFT:
            self.go_left(dungeon)
        if move == Movement.RIGHT:
            self.go_right(dungeon)
        return GameState.NONE

    @staticmethod
    def do_action(next_cell):
        prob = rand.random()
        sump = 0
        for e in next_cell:
            sump += e[0]
            if prob <= sump:
                return e
        return ()

def get_next_player_state(cell, dungeon, state):
    if cell == Cell.EMPTY:
        return [(1, PlayerState.STAY)]
    if cell == Cell.START:
        return [(1, PlayerState.WIN)] if state.treasure else [(1, PlayerState.STAY)]
    if cell == Cell.KEY:
        return [(1, PlayerState.GET_KEY)] if not state.key else [(1, PlayerState.STAY)]
    if cell == Cell.SWORD:
        return [(1, PlayerState.GET_SWORD)] if not state.sword else [(1, PlayerState.STAY)]
    if cell == Cell.TREASURE:
        return [(1, PlayerState.GET_TREASURE)] if state.key and not state.treasure else [(1, PlayerState.STAY)]
    if cell == Cell.CRACKS:
        return [(1, PlayerState.DEAD)]
    if cell == Cell.ENEMY:
        return [(0.7, PlayerState.STAY), (0.3, PlayerState.DEAD)] if not state.sword else [(1, PlayerState.STAY)]
    if cell == Cell.TRAP:
        return [(0.6, PlayerState.STAY), (0.1, PlayerState.DEAD), (0.3, PlayerState.MOVE, (dungeon.x - 1, dungeon.y - 1))]
    if cell == Cell.PLATFORM:
        nb_wall_not = 0
        possible_cell = []
        for (i, j) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if not dungeon.is_wall(state.pos[0] + i, state.pos[1] + j):
                nb_wall_not += 1
                possible_cell.append((state.pos[0] + i, state.pos[1] + j))
        res = []
        for c in possible_cell:
            res.append((1 / nb_wall_not, PlayerState.MOVE, c))
        return res
    if cell == Cell.PORTAL:
        nb_wall_not = 0
        possible_cell = []
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j) and (i, j) != state.pos:
                    nb_wall_not += 1
                    possible_cell.append((i, j))
        res = []
        for c in possible_cell:
            res.append((1 / nb_wall_not, PlayerState.MOVE, c))
        return res
    return []

# What are the next states (with their probabilities) if we move to cell at cellPos from state in dungeon.
def get_next_game_state(cell, cellPos, dungeon, state):
    if cell in [Cell.EMPTY, Cell.START]:
        return [(1, State(state.treasure, state.key, state.sword, cellPos))]
    elif cell == Cell.KEY:
        return [(1, State(state.treasure, True, state.sword, cellPos))]
    elif cell == Cell.SWORD:
        return [(1, State(state.treasure, state.key, True, cellPos))]
    elif cell == Cell.TREASURE and state.key:
        return [(1, State(True, state.key, state.sword, cellPos))]
    elif cell == Cell.TREASURE:
        return [(1, State(state.treasure, state.key, state.sword, cellPos))]
    elif cell == Cell.CRACKS:
        return [(1, State(state.treasure, state.key, state.sword, (-9, -9)))]
    elif cell == Cell.ENEMY and state.sword:
        return [(0.7, State(state.treasure, state.key, state.sword, cellPos)), \
        (0.3, State(state.treasure, state.key, state.sword, (-9, -9)))] 
    elif cell == Cell.ENEMY:
        return [(1, State(state.treasure, state.key, state.sword, cellPos))]
    elif cell == Cell.TRAP:
        return [(0.6, State(state.treasure, state.key, state.sword, cellPos)), \
        (0.1, State(state.treasure, state.key, state.sword, (-9, -9))), \
        (0.3, State(state.treasure, state.key, state.sword, (dungeon.x - 1, dungeon.y - 1)))]
    elif cell == Cell.PLATFORM:
        possible_states = []
        for move in [Movement.LEFT, Movement.RIGHT, Movement.TOP, Movement.DOWN]:
            if not dungeon.is_wall(cellPos[0] + move.value[0], cellPos[1] + move.value[1]):
                possible_states.append(State(state.treasure, state.key, state.sword, 
                    (cellPos[0] + move.value[0], cellPos[1] + move.value[1])))
        res = []
        for s in possible_states:
            res.append((1 / len(possible_states), s))
        return res
    if cell == Cell.PORTAL:
        possible_states = []
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j) and (i, j) != state.pos:
                    possible_states.append(State(state.treasure, state.key, state.sword, (i, j)))
        res = []
        for s in possible_states:
            res.append((1 / len(possible_states), s))
        return res
    return []
