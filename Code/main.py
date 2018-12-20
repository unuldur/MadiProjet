from pdm import PDM, PdmMovement, PDM2
from graphics import Graphics
from player import Player, GameState
from solverPDM import *
from dungeon import random_dungeon_generation, load_dungeon
import argparse
import time
import sys
import pygame
import copy

def print_PDM(dungeon, g, gurobi = False):
    p = Player(dungeon.x - 1, dungeon.y - 1)
    g.print(dungeon, p)
    pdm = PDM(dungeon)
    print("PDM generated with " + str(len(pdm.nodes.keys())) + " nodes.")
    if gurobi:
        strat, value = pl_algo(dungeon, pdm, 0.9)
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
            return False
        if gameState == GameState.WIN:
            g.print_message("Well done ! You brought the treasure back home.")
            return True
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

def countNumTryBeforeWin(dungeon, g, gurobi = False):
    nbTry = 1
    while not print_PDM(copy.deepcopy(dungeon), g, gurobi):
        nbTry += 1
    print("Dungeon solved in " + str(nbTry) + " attempts.")

def main():
    print("==========================================================")
    print("|                       Magic Maze                       |")
    print("==========================================================")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help = "The dungeon file to play with.")
    parser.add_argument('--pdmIteVal', action = 'store_true', help = "Solve the dungeon with value iteration.")
    parser.add_argument('--pdmGurobi', action = 'store_true', help = "Solve the dungeon with Gurobi.")
    parser.add_argument('--count', action = 'store_true', help = "Try again and again to win the game.")
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
        if args['count']:
            countNumTryBeforeWin(dungeon, g)
        else:
            print_PDM(dungeon, g)
    elif (args['pdmGurobi']):
        g.print_footer("Welcome to Magic Maze, you are looking at the moves computed by the PDM resolution.")
        if args['count']:
            countNumTryBeforeWin(dungeon, g, True)
        else:
            print_PDM(dungeon, g, True)
    else:
        g.print_footer("Welcome to Magic Maze, use keyboard arrows to play.")
        print_playerInput(dungeon, g)
    time.sleep(1)

main()