from gameState import GameState
from movement import Movement
from cell import cell_movement, Cell
import random as rand

from etat import Etat


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

    def do_move(self, input_method, dungeon):
        next_cell = cell_movement(dungeon.dungeon[self.x, self.y], dungeon, self)
        next_move = self.do_action(next_cell)
        if next_move[1] == Etat.MOVE:
            self.x = next_move[2][0]
            self.y = next_move[2][1]
            return GameState.NONE
        if next_move[1] == Etat.WIN:
            return GameState.WIN
        if next_move[1] == Etat.DEAD:
            return GameState.DEAD
        if next_move[1] == Etat.GET_TREASURE:
            self.treasure = True
            dungeon.dungeon[self.x, self.y] = Cell.EMPTY
        if next_move[1] == Etat.GET_SWORD:
            self.sword = True
            dungeon.dungeon[self.x, self.y] = Cell.EMPTY
        if next_move[1] == Etat.GET_KEY:
            self.key = True
            dungeon.dungeon[self.x, self.y] = Cell.EMPTY
        if next_move[1] == Etat.KILL_ENEMY:
            dungeon.dungeon[self.x, self.y] = Cell.EMPTY
        move = input_method.get_next_move()
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
