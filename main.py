from PDM import PDM
from dungeonLoader import *
from gameState import GameState
from graphics import Graphics
from pdm_movement import PdmMovement
from player import Player
from IterationPdm import *

dungeon = load_dungeon("dungeon1")
dungeon = random_dungeon_generation(3, 3)
pdm = PDM(dungeon)
strat = iteration_algo(dungeon, pdm, 0.3, 0.001)
pdmMove = PdmMovement(strat)
#pdm.print()
g = Graphics(400, 600)
p = Player(dungeon.x - 1, dungeon.y - 1)
g.print_transition(dungeon, p, pdmMove)
finish = False
while g.print_transition(dungeon, p, pdmMove) and not finish:

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

