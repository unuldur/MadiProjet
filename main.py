from PDM import PDM
from dungeonLoader import *
from gameState import GameState
from graphics import Graphics
from pdm_movement import PdmMovement
from player import Player
from IterationPdm import *
import argparse
import time
import sys
import pygame

def print_PDM(dungeon, g, gurobi = False):
    p = Player(dungeon.x - 1, dungeon.y - 1)
    g.print(dungeon, p)
    pdm = PDM(dungeon)
    if gurobi:
        # ICI METTRE LE CALCUL DU PDM PAR GUROBI !!!!!!!!!!!!!
    else:
        strat, value = iteration_algo(dungeon, pdm, 1, 0.001)
    pdmMove = PdmMovement(strat)
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
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
            sys.exit()

def print_playerInput(dungeon, g):
    p = Player(dungeon.x - 1, dungeon.y - 1)
    finish = False
    while not finish:
        g.print(dungeon, p)
        gameState = p.do_move(g, dungeon)
        if gameState == GameState.DEAD:
            g.print_message("Too bad, you are dead and the treasure is not yours.")
            finish = True
        if gameState == GameState.WIN:
            g.print_message("Well done ! You brought the treasure back home.")
            finish = True
        if gameState == GameState.FINISH:
            sys.exit()

def main():
    print("==========================================================")
    print("|                       Magic Maze                       |")
    print("==========================================================")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help = "The dungeon file to play with.")
    parser.add_argument('--pdmIteVal', action = 'store_true', help = "Solve the dungeon with value iteration.")
    parser.add_argument('--pdmGurobi', action = 'store_true', help = "Solve the dungeon with Gurobi.")
    args = vars(parser.parse_args())

    dungeon = random_dungeon_generation(6, 6)
    if (args['d']):
        print("Loading dungeon " + args['d'] + ".")
        dungeon = load_dungeon(args['d'])
    else:
        print("No dungeon file give, a random dungeon is being creating. Here are the options if you were looking for them.")
        parser.print_help()

    g = Graphics(800, 1000, dungeon)

    if (args['pdmIteVal']):
        g.print_footer("Welcome to Magic Maze, you are looking at the moves computed by the PDM resolution.")
        print_PDM(dungeon, g)
    else:
        g.print_footer("Welcome to Magic Maze, use keyboard arrows to play.")
        print_playerInput(dungeon, g)

    time.sleep(3)

main()