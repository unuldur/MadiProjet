from PDM import PDM
from dungeonLoader import *
from gameState import GameState
from graphics import Graphics
from pdm_movement import PdmMovement
from player import Player
from IterationPdm import *

dungeon = load_dungeon("dungeon1")
#dungeon = random_dungeon_generation(4, 4)
pdm = PDM(dungeon)
strat, value = iteration_algo(dungeon, pdm, 1, 0.001)
pdmMove = PdmMovement(strat)
#pdm.print()
g = Graphics(800, 1000)
p = Player(dungeon.x - 1, dungeon.y - 1)
g.print_transition(dungeon, p, pdmMove, value)
finish = False
while g.print(dungeon, p) and not finish:

    gameState = p.do_move(pdmMove, dungeon)
    if gameState == GameState.DEAD:
        print("You died potato")
        finish = True
    if gameState == GameState.WIN:
        print("GG! You win! You are just lucky in fact.")
        finish = True
    if gameState == GameState.FINISH:
        print("Stop game")
        finish = True


