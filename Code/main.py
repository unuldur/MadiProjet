from pdm import PDM, PdmMovement
from graphics import Graphics
from player import Player, GameStatus
from solverPDM import *
from dungeon import random_dungeon_generation, load_dungeon
from qlearning import learningPDM
import argparse
import time
import sys
import pygame
import copy

# Run a episode for the qLearning
def try_qLearning(dungeon, g, pdm):
    p = Player(dungeon.x - 1, dungeon.y - 1)
    g.print(dungeon, p)
    currentState = p.get_state()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Play the move and update the model given the new state reached
        previousState = currentState
        gameState = p.move(pdm, dungeon, g)
        currentState = p.get_state()
        pdm.addObservation(previousState, currentState)

        if gameState == GameStatus.WIN:
            g.print_message("Well done ! You brought the treasure back home.")
            return True
        elif gameState == GameStatus.DEAD:
            g.print_message("Too bad, you are dead and the treasure is not yours.")
            return False
        elif gameState == GameStatus.FINISH:
            sys.exit()

# Run episodes of qLearning until a win
def print_qLearning(dungeon, g):
    pdm = learningPDM(dungeon, 0.1)
    nbTry = 1
    while not try_qLearning(copy.deepcopy(dungeon), g, pdm):
        nbTry += 1
    print("Dungeon solved in " + str(nbTry) + " attempts using Q-learning.")

# Run and print the PDM solver for the dungeon, uses Gurobi if gurobi = True, else iteration value algorithm
def print_PDM(dungeon, g, gurobi = False):
    p = Player(dungeon.x - 1, dungeon.y - 1)
    g.print(dungeon, p)
    pdm = PDM(dungeon)
    print("PDM generated with " + str(len(pdm.nodes.keys())) + " nodes.")

    # Compute the policy using iteration value algorithm or integer programming
    if gurobi:
        strat, value = pl_algo(dungeon, pdm, 0.9)
    else:
        strat, value = iteration_algo(dungeon, pdm, 1, 0.001)
    pdmMove = PdmMovement(strat)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Play the moves accordingly to the policy
        gameState = p.move(pdmMove, dungeon, g, pdmMove)
        if gameState == GameStatus.DEAD:
            g.print_message("Too bad, you are dead and the treasure is not yours.")
            return False
        if gameState == GameStatus.WIN:
            g.print_message("Well done ! You brought the treasure back home.")
            return True
        if gameState == GameStatus.FINISH:
            sys.exit()

# Run and print the game played by the user's inputs
def print_playerInput(dungeon, g):
    p = Player(dungeon.x - 1, dungeon.y - 1)
    finish = False
    while not finish:
        gameState = p.move(g, dungeon, g)
        if gameState == GameStatus.DEAD:
            g.print_message("Too bad, you are dead and the treasure is not yours.")
            finish = True
        if gameState == GameStatus.WIN:
            g.print_message("Well done ! You brought the treasure back home.")
            finish = True
        if gameState == GameStatus.FINISH:
            sys.exit()

# Run a PDM solver until a win
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
    parser.add_argument('-d', type = int, help = "The dungeon file to play with.")
    parser.add_argument('-r', help = "Use a square random dungeon of the given size.")
    parser.add_argument('--pdmIteVal', action = 'store_true', help = "Solve the dungeon with value iteration.")
    parser.add_argument('--pdmGurobi', action = 'store_true', help = "Solve the dungeon with Gurobi.")
    parser.add_argument('--qLearn', action = 'store_true', help = "Solve the dungeon with Q-Learning.")
    parser.add_argument('--count', action = 'store_true', help = "Try again and again to win the game.")
    args = vars(parser.parse_args())

    if args['d']:
        print("Loading dungeon " + args['d'] + ".")
        dungeon = load_dungeon(args['d'])
    elif args['r']:
        try:
            r = max(int(args['r']), 2)
        except Exception as e:
            print("An exception \"" + str(e) + "\" has occured, did you give an integer as -r argument ?")
            sys.exit()
        dungeon = random_dungeon_generation(r, r)
    else:
        print("No dungeon file give, a random dungeon is being creating. Here are the options if you were looking for them.")
        parser.print_help()
        dungeon = random_dungeon_generation(5, 5)

    g = Graphics(800, 1000, dungeon)

    if args['pdmIteVal']:
        g.print_footer("Welcome to Magic Maze, you are looking at the moves computed by the PDM resolution.")
        if args['count']:
            countNumTryBeforeWin(dungeon, g)
        else:
            print_PDM(dungeon, g)
    elif args['pdmGurobi']:
        g.print_footer("Welcome to Magic Maze, you are looking at the moves computed by the PDM resolution.")
        if args['count']:
            countNumTryBeforeWin(dungeon, g, True)
        else:
            print_PDM(dungeon, g, True)
    elif args['qLearn']:
        g.print_footer("Welcome to Magic Maze, you are looking at the moves computed using Q-Learning.")
        print_qLearning(dungeon, g)
    else:
        g.print_footer("Welcome to Magic Maze, use keyboard arrows to play.")
        print_playerInput(dungeon, g)
    time.sleep(1)

main()