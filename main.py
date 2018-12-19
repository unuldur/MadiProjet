from PDM import PDM
from dungeonLoader import *
from gameState import GameState
from graphics import Graphics
from pdm_movement import PdmMovement
from player import Player
from IterationPdm import *
import time

def print_PDM(dungeon, g):
    pdm = PDM(dungeon)
    strat, value = iteration_algo(dungeon, pdm, 1, 0.001)
    pdmMove = PdmMovement(strat)
    p = Player(dungeon.x - 1, dungeon.y - 1)
    finish = False
    while not finish:
        g.print(dungeon, p)
        g.print_PDM_strat(dungeon, p, pdmMove)
        gameState = p.do_move(pdmMove, dungeon)
        if gameState == GameState.DEAD:
            g.print_message("Too bad, you are dead and the treasure is not yours.")
            finish = True
        if gameState == GameState.WIN:
            g.print_message("Well done ! You brought the treasure back home.")
            finish = True
        if gameState == GameState.FINISH:
            g.print_message("The game has stopped unexpectedly.")
            finish = True

# dungeon = load_dungeon("dungeon1")
dungeon = random_dungeon_generation(6, 6)

g = Graphics(800, 1000)
g.print_footer("Welcome to Magic Maze, press space to lauch the program.")

print_PDM(dungeon, g)

time.sleep(5)