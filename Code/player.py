from enum import IntEnum, Enum
from dungeon import Cell
from state import State
import random as rand

# Enumeration for possible Game status
class GameStatus(IntEnum):
    WIN = 0
    DEAD = 1
    NONE = 2
    FINISH = 3

# Enumeration for possible movements
class Movement(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    TOP = (0, -1)
    DOWN = (0, 1)
    STOP = ()

# Enumeration for possible player status
class PlayerStatus(IntEnum):
    MOVE = 1
    DEAD = 2
    STAY = 3
    GET_KEY = 4
    GET_SWORD = 5
    WIN = 6
    GET_TREASURE = 7

# Class of the player, contains its position (x, y) and what he owns: key, sword, treasure
# Special position (-9, -9) means the adventurer is dead
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.key = False
        self.sword = False
        self.treasure = False

    # Move the player in a given direction
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

    # Teleports the player
    def set_new_pos(self, x, y):
        self.x = x
        self.y = y

    # Returns the current state of the player as a game state
    def get_state(self):
        return State(self.treasure, self.key, self.sword, (self.x, self.y))

    # Computes the move of the player give the input_method (call get_next_move(state) on the object), moves the player
    # and applied the effects of new cell
    def move(self, input_method, dungeon, g, pdmMove = None):
        # Computes the move and applies it
        move = input_method.get_next_move(self.get_state())
        if move == Movement.STOP:
            return GameStatus.FINISH
        elif move == Movement.DOWN:
            self.go_down(dungeon)
        elif move == Movement.TOP:
            self.go_up(dungeon)
        elif move == Movement.LEFT:
            self.go_left(dungeon)
        elif move == Movement.RIGHT:
            self.go_right(dungeon)
        # Update graphics (if PDM policy given, draw the arrows)
        if pdmMove != None:
            g.print_PDM_strat(dungeon, self, pdmMove)
        else:
            g.print(dungeon, self)

        # Computes all the possible reactions of the current cell with their probability
        reactions = get_next_player_status(dungeon.cells[self.x, self.y], dungeon, self.get_state())
        # Select of reaction
        selectedReaction = self.selectReaction(reactions)
        # As long as there are reactions, applies it (typically when a portal teleports to another portal)
        while selectedReaction[1] != PlayerStatus.STAY:
            if selectedReaction[1] == PlayerStatus.MOVE:
                self.x = selectedReaction[2][0]
                self.y = selectedReaction[2][1]
            elif selectedReaction[1] == PlayerStatus.WIN:
                return GameStatus.WIN
            elif selectedReaction[1] == PlayerStatus.DEAD:
                self.x = -9
                self.y = -9
                return GameStatus.DEAD
            elif selectedReaction[1] == PlayerStatus.GET_TREASURE:
                self.treasure = True
                dungeon.cells[self.x, self.y] = Cell.EMPTY
            elif selectedReaction[1] == PlayerStatus.GET_SWORD:
                self.sword = True
                dungeon.cells[self.x, self.y] = Cell.EMPTY
            elif selectedReaction[1] == PlayerStatus.GET_KEY:
                self.key = True
                dungeon.cells[self.x, self.y] = Cell.EMPTY

            # Update graphics
            if pdmMove != None:
                g.print_PDM_strat(dungeon, self, pdmMove)
            else:
                g.print(dungeon, self)

            # Computes new possible reactions
            reactions = get_next_player_status(dungeon.cells[self.x, self.y], dungeon, self.get_state())
            selectedReaction = self.selectReaction(reactions)

        return GameStatus.NONE

    # Selects a reaction at random following their distribution 
    def selectReaction(self, reactions):
        prob = rand.random()
        sump = 0
        for e in reactions:
            sump += e[0]
            if prob <= sump:
                return e
        return ()

# Returns the next player status if he moves to cell from state
def get_next_player_status(cell, dungeon, state):
    if cell == Cell.EMPTY:
        return [(1, PlayerStatus.STAY)]
    if cell == Cell.START:
        return [(1, PlayerStatus.WIN)] if state.treasure else [(1, PlayerStatus.STAY)]
    if cell == Cell.KEY:
        return [(1, PlayerStatus.GET_KEY)] if not state.key else [(1, PlayerStatus.STAY)]
    if cell == Cell.SWORD:
        return [(1, PlayerStatus.GET_SWORD)] if not state.sword else [(1, PlayerStatus.STAY)]
    if cell == Cell.TREASURE:
        return [(1, PlayerStatus.GET_TREASURE)] if state.key and not state.treasure else [(1, PlayerStatus.STAY)]
    if cell == Cell.CRACKS:
        return [(1, PlayerStatus.DEAD)]
    if cell == Cell.ENEMY:
        return [(0.7, PlayerStatus.STAY), (0.3, PlayerStatus.DEAD)] if not state.sword else [(1, PlayerStatus.STAY)]
    if cell == Cell.TRAP:
        return [(0.6, PlayerStatus.STAY), (0.1, PlayerStatus.DEAD), (0.3, PlayerStatus.MOVE, (dungeon.x - 1, dungeon.y - 1))]
    if cell == Cell.PLATFORM:
        # Find all neightbours that are not walls
        nb_not_wall = 0
        possible_cell = []
        for (i, j) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if not dungeon.is_wall(state.pos[0] + i, state.pos[1] + j):
                nb_not_wall += 1
                possible_cell.append((state.pos[0] + i, state.pos[1] + j))
        res = []
        for c in possible_cell:
            res.append((1 / nb_not_wall, PlayerStatus.MOVE, c))
        return res
    if cell == Cell.PORTAL:
        # Find all cells that are not walls
        nb_not_wall = 0
        possible_cell = []
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j) and (i, j) != state.pos:
                    nb_not_wall += 1
                    possible_cell.append((i, j))
        res = []
        for c in possible_cell:
            res.append((1 / nb_not_wall, PlayerStatus.MOVE, c))
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
        return [(1, State(state.treasure, state.key, state.sword, cellPos))]
    elif cell == Cell.ENEMY:
        return [(0.7, State(state.treasure, state.key, state.sword, cellPos)), \
        (0.3, State(state.treasure, state.key, state.sword, (-9, -9)))] 
    elif cell == Cell.TRAP:
        return [(0.6, State(state.treasure, state.key, state.sword, cellPos)), \
        (0.1, State(state.treasure, state.key, state.sword, (-9, -9))), \
        (0.3, State(state.treasure, state.key, state.sword, (dungeon.x - 1, dungeon.y - 1)))]
    elif cell == Cell.PLATFORM:
        # Find all neightbours that are not walls
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
        # Find all cells that are not walls
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