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
    HURT = 8

# Class of the player, contains its position (x, y) and what he owns: key, sword, treasure
# Special position (-9, -9) means the adventurer is dead
class Player:
    def __init__(self, x, y, maxLife, g):
        self.x = x
        self.y = y
        self.key = False
        self.sword = False
        self.treasure = False
        self.life = maxLife
        self.g = g

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

    # Reduce player's life by one
    def changeLife(self, newLife, display):
        self.life = newLife
        if display: self.g.update_footer_life(self.life)

    # Teleports the player
    def set_new_pos(self, x, y):
        self.x = x
        self.y = y

    # Returns the current state of the player as a game state
    def get_state(self):
        return State(self.treasure, self.key, self.sword, (self.x, self.y), self.life)

    # Computes the move of the player give the input_method (call get_next_move(state) on the object), moves the player
    # and applied the effects of new cell
    def move(self, input_method, dungeon, pdmMove = None, pdmVal = None, display = True):
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
        if display:
            if pdmMove != None:
                self.g.print_PDM_strat(dungeon, self, pdmMove)
            if pdmVal != None:
                self.g.print_PDM_values(dungeon, self, pdmVal)
            if pdmMove == None and pdmVal == None:
                self.g.print(dungeon, self)

        # Computes all the possible reactions of the current cell with their probability
        reactions = get_position_reaction(dungeon.cells[self.x, self.y], dungeon, self.get_state())
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
                self.changeLife(0, display)
                return GameStatus.DEAD
            elif selectedReaction[1] == PlayerStatus.HURT:
                self.changeLife(self.life - 1, display)
                if self.life == 0:
                    return GameStatus.DEAD
                break
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
            if display:
                if pdmMove != None:
                    self.g.print_PDM_strat(dungeon, self, pdmMove)
                if pdmVal != None:
                    self.g.print_PDM_values(dungeon, self, pdmVal)
                if pdmMove == None and pdmVal == None:
                    self.g.print(dungeon, self)

            # Computes new possible reactions
            reactions = get_position_reaction(dungeon.cells[self.x, self.y], dungeon, self.get_state())
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
        print('Did not find any reactions in ' + str(reactions))
        return (1, PlayerStatus.STAY)

# Returns the next player status if he moves to cell from state
def get_position_reaction(cell, dungeon, state):
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
        return [(0.7, PlayerStatus.STAY), (0.3, PlayerStatus.HURT)] if not state.sword else [(1, PlayerStatus.STAY)]
    if cell == Cell.TRAP:
        return [(0.6, PlayerStatus.STAY), (0.1, PlayerStatus.HURT), (0.3, PlayerStatus.MOVE, (dungeon.x - 1, dungeon.y - 1))]
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

    print("No reaction found for cell " + str(cell))
    return []