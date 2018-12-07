from dungeon import Dungeon
from dungeonLoader import *
from gameState import GameState
from graphics import Graphics
from player import Player

dungeon = load_dungeon("dungeon1")
dungeon = random_dungeon_generation(8, 8)

g = Graphics(400, 600)
p = Player(dungeon.x - 1, dungeon.y - 1)
finish = False
while g.print(dungeon, p) and not finish:

    gameState = p.do_move(g, dungeon)
    if gameState == GameState.DEAD:
        print("You died potato")
        finish = True
    if gameState == GameState.WIN:
        print("GG! You win! You are just lucky in fact.")
        finish = True
    if gameState == GameState.FINISH:
        print("Stop game")
        finish = True

