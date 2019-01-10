from pdm import PDM, PdmMovement
from graphics import Graphics
from player import Player, GameStatus
from solverPDM import *
from dungeon import random_dungeon_generation, load_dungeon
from qlearning import learningPDM
from bench import bench
import argparse
import time
import sys
import pygame
import copy

# Run a episode for the qLearning
def try_qLearning(dungeon, g, pdm, maxLife, dis):
    p = Player(dungeon.x - 1, dungeon.y - 1, maxLife, g)
    if dis:
        g.print(dungeon, p)
        g.update_footer_life(p.life)
    currentState = p.get_state()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Play the move and update the model given the new state reached
        previousState = currentState
        gameState = p.move(pdm, dungeon, display = dis)
        currentState = p.get_state()
        pdm.addObservation(previousState, currentState)

        if gameState == GameStatus.WIN:
            if dis: g.print_message("Well done ! You brought the treasure back home.")
            return True
        elif gameState == GameStatus.DEAD:
            if dis: g.print_message("Too bad, you are dead and the treasure is not yours.")
            return False
        elif gameState == GameStatus.FINISH:
            sys.exit()

# Run episodes of qLearning until a win
def print_qLearning(dungeon, g, maxLife):
    previousSpeed = g.waitingTime
    g.waitingTime = 1
    pdm = learningPDM(dungeon, 0.1, maxLife)
    numEpisodes = 10000
    for i in range(numEpisodes):
        try_qLearning(copy.deepcopy(dungeon), g, pdm, maxLife, False)
        if i % (numEpisodes / 10) == 0:
            print("QLearning " + str(i) + " episodes done")
    nbTry = 1
    g.waitingTime = previousSpeed
    while not try_qLearning(copy.deepcopy(dungeon), g, pdm, maxLife, True):
        nbTry += 1
    print("Dungeon solved in " + str(nbTry) + " attempts using Q-learning.")

def run_PDM(dungeon, g, maxLife, pdmMove, value):
    p = Player(dungeon.x - 1, dungeon.y - 1, maxLife, g)
    g.print(dungeon, p)

    # g.screenShot(dungeon.name)
    # n = dungeon.name
    # dungeon.name = n + "_sol"
    # g.print_PDM_strat(dungeon, p, pdmMove)
    # p.key = True
    # dungeon.name = n + "_solKey"
    # g.print_PDM_strat(dungeon, p, pdmMove)
    # p.treasure = True
    # dungeon.name = n + "_solTres"
    # g.print_PDM_strat(dungeon, p, pdmMove)
    # sys.exit()

    g.update_footer_life(p.life)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Play the moves accordingly to the policy
        gameState = p.move(pdmMove, dungeon, pdmMove)
        if gameState == GameStatus.DEAD:
            g.print_message("Too bad, you are dead and the treasure is not yours.")
            return False
        if gameState == GameStatus.WIN:
            g.print_message("Well done ! You brought the treasure back home.")
            return True
        if gameState == GameStatus.FINISH:
            sys.exit()

# Run and print the PDM solver for the dungeon, uses Gurobi if gurobi = True, else iteration value algorithm
def print_PDM(dungeon, g, maxLife, infinite, gurobi = False):
    pdm = PDM(dungeon, maxLife)
    print("PDM generated with " + str(len(pdm.nodes.keys())) + " nodes.")

    # Compute the policy using iteration value algorithm or integer programming
    if gurobi:
        strat, value = pl_algo(dungeon, pdm, 0.9)
    else:
        strat, value = iteration_algo(dungeon, pdm, 1, 1)
    pdmMove = PdmMovement(strat)

    if infinite:
        nbTry = 1
        while not run_PDM(copy.deepcopy(dungeon), g, maxLife, pdmMove, value):
            nbTry += 1
        print("Dungeon solved in " + str(nbTry) + " attempts.")
    else:
        run_PDM(dungeon, g, maxLife, pdmMove, value)
    

# Run and print the game played by the user's inputs
def print_playerInput(dungeon, g, maxLife):
    p = Player(dungeon.x - 1, dungeon.y - 1, maxLife, g)
    g.print(dungeon, p)
    finish = False
    while not finish:
        gameState = p.move(g, dungeon)
        if gameState == GameStatus.DEAD:
            g.print_message("Too bad, you are dead and the treasure is not yours.")
            finish = True
        if gameState == GameStatus.WIN:
            g.print_message("Well done ! You brought the treasure back home.")
            finish = True
        if gameState == GameStatus.FINISH:
            sys.exit()

def main():
    print("==========================================================")
    print("|                       Magic Maze                       |")
    print("==========================================================")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help = "The dungeon file to play with.")
    parser.add_argument('-r', type = int, help = "Use a square random dungeon of the given size.")
    parser.add_argument('-s', type = int, help = "Set the waiting time between moves in milliseconds.")
    parser.add_argument('-l', type = int, help = "Set the starting life of the player.")
    parser.add_argument('--pdmIteVal', action = 'store_true', help = "Solve the dungeon with value iteration.")
    parser.add_argument('--pdmGurobi', action = 'store_true', help = "Solve the dungeon with Gurobi.")
    parser.add_argument('--qLearn', action = 'store_true', help = "Solve the dungeon with Q-Learning.")
    parser.add_argument('--infinite', action = 'store_true', help = "Try again and again to win the game.")
    parser.add_argument('--bench', action = 'store_true', help = "Run the benchs.")
    args = vars(parser.parse_args())

    if args['bench']:
        bench()
        return

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

    try:
        s = max(int(args['s']), 1)
    except Exception as e:
        s = 500

    try:
        maxLife = max(int(args['l']), 1)
    except Exception as e:
        maxLife = 1

    g = Graphics(800, 1000, dungeon, s, maxLife, maxLife)

    if args['pdmIteVal']:
        g.print_footer("Welcome to Magic Maze, you are looking at the moves computed by the PDM resolution.")
        if args['infinite']:
            print_PDM(dungeon, g, maxLife, True)
        else:
            print_PDM(dungeon, g, maxLife, False)
    elif args['pdmGurobi']:
        g.print_footer("Welcome to Magic Maze, you are looking at the moves computed by the PDM resolution.")
        if args['infinite']:
            print_PDM(dungeon, g, maxLife, True, True)
        else:
            print_PDM(dungeon, g, maxLife, False, True)
    elif args['qLearn']:
        g.print_footer("Welcome to Magic Maze, you are looking at the moves computed using Q-Learning.")
        print_qLearning(dungeon, g, maxLife)
    else:
        g.print_footer("Welcome to Magic Maze, use keyboard arrows to play.")
        print_playerInput(dungeon, g, maxLife)
    time.sleep(1)

main()