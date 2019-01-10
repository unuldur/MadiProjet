from dungeon import *
from player import Player, GameStatus
from pdm import PDM, PdmMovement
from qlearning import learningPDM
from solverPDM import *
from time import time
from os import listdir
from os.path import isfile, join
from graphics import Graphics
import matplotlib.pyplot as plt
import copy
import pygame

# Generate a set of instance of dungeon
def generateDungeons(numInstBySize, maxSize):
	dungeonFiles = [f for f in listdir("../Dungeons") if isfile(join("../Dungeons/", f))]
	for f in dungeonFiles:
		os.unlink("../Dungeons/" + f)
	for i in range(2, maxSize):
		for j in range(numInstBySize):
			d = random_dungeon_generation(i, i)
			d.write("../Dungeons/D_" + str(i) + "_" + str(i) + "_num_" + str(j))

# Read all the dungeon in the folder Dungeons
def getDungeons():
	dungeonFiles = [f for f in listdir("../Dungeons") if isfile(join("../Dungeons/", f))]
	dungeons = []
	for d in dungeonFiles:
		dungeons.append(load_dungeon(join("../Dungeons/", d)))
	return dungeons

# Get the time required to solve a instance by each algorithm
def getSolveTime(dungeon, gurobi, maxLife, g):
	p = Player(dungeon.x - 1, dungeon.y - 1, maxLife, g)
	pdm = PDM(dungeon, maxLife)
	startTime = time()
	# Compute the policy using iteration value algorithm or integer programming
	if gurobi:
		strat, value = pl_algo(dungeon, pdm, 0.9, quiet = True)
	else:
		strat, value = iteration_algo(dungeon, pdm, 1, 1)
	return time() - startTime

# Get the solve timing for all instances for each algorithm
def benchSolveTime(numTry, maxLife):
	dungeons = getDungeons()
	timeGurobi = dict()
	timeIteVal = dict()
	numDungeon = 1
	for dungeon in dungeons:
		print("Bench dungeon " + str(numDungeon) + " out of " + str(len(dungeons)))
		g = Graphics(800, 1000, dungeon, 5, maxLife, maxLife)
		timeGurobi[dungeon] = 0.0
		timeIteVal[dungeon] = 0.0
		for i in range(numTry):
			timeGurobi[dungeon] = timeGurobi[dungeon] + getSolveTime(dungeon, True, maxLife, g)
			timeIteVal[dungeon] = timeIteVal[dungeon] + getSolveTime(dungeon, False, maxLife, g)
		timeGurobi[dungeon] = timeGurobi[dungeon] / numTry
		timeIteVal[dungeon] = timeIteVal[dungeon] / numTry
		numDungeon += 1
	return (timeIteVal, timeGurobi)

# Plot the solve timing
def plotSolveTime(maxSize, numTry, numInstBySize, maxLife):
	print("Benching Time")
	(timeIteVal, timeGurobi) = benchSolveTime(numTry, maxLife)
	meanBySizeIteVal = []
	meanBySizeGurobi = []
	for i in range(maxSize - 2):
		meanBySizeGurobi.append(0)
		meanBySizeIteVal.append(0)
	for (k, val) in timeIteVal.items():
		meanBySizeIteVal[k.x - 2] = meanBySizeIteVal[k.x - 2] + val
	for (k, val) in timeGurobi.items():
		meanBySizeGurobi[k.x - 2] = meanBySizeGurobi[k.x - 2] + val
	for i in range(maxSize - 2):
		meanBySizeGurobi[i] = meanBySizeGurobi[i] / numInstBySize
		meanBySizeIteVal[i] = meanBySizeIteVal[i] / numInstBySize

	file = open("DataTime", "w")
	file.write(str(meanBySizeGurobi) + "\n")
	file.write(str(meanBySizeIteVal) + "\n")
	file.close()

	plt.close('all')
	plt.figure()
	plt.plot(range(2, maxSize, 1), meanBySizeGurobi, label = "PDM Gurobi")
	plt.plot(range(2, maxSize, 1), meanBySizeIteVal, label = "PDM IteVal")
	plt.legend(loc = 0)
	plt.suptitle("Solving time for each algorithm")
	plt.xlabel('Dungeon size')
	plt.ylabel('Mean solving time')
	plt.savefig("../Plot/PlotSolvingTime.png", dpi = 200)

# Get the number of attempt before a win for a dungeon
def getNumTryBeforWinPDM(dungeon, g, gurobi, qLearn, maxLife, numEpisode):
	count = 1
	won = False
	# Initialize the algorithm and compute the solution
	if not qLearn:
		pdm = PDM(dungeon, maxLife)
		if gurobi:
			policy, value = pl_algo(dungeon, pdm, 0.9, quiet = True)
		else:
			policy, value = iteration_algo(dungeon, pdm, 1, 1)
		pdmMove = PdmMovement(policy)
	else:
		pdm = learningPDM(dungeon, 0.1, maxLife)
		for i in range(numEpisode):
			d = copy.deepcopy(dungeon)
			p = Player(d.x - 1, d.y - 1, maxLife, g)
			currentState = p.get_state()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
				previousState = currentState
				gameState = p.move(pdm, d, display = False)
				currentState = p.get_state()
				pdm.addObservation(previousState, currentState)
				if gameState == GameStatus.WIN or gameState == GameStatus.DEAD:
					break

	# Loop until a win
	while not won and count < 100:
		d = copy.deepcopy(dungeon)
		p = Player(d.x - 1, d.y - 1, maxLife, g)
		dead = False
		if qLearn:
			currentState = p.get_state()
		numMove = 0
		# Loop until the game is not finished
		while not dead:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			if qLearn:
				previousState = currentState
				gameState = p.move(pdm, d, display = False)
				currentState = p.get_state()
				pdm.addObservation(previousState, currentState)
			else:
				gameState = p.move(pdmMove, d, pdmMove, display = False)

			if gameState == GameStatus.DEAD:
				dead = True
			if gameState == GameStatus.WIN:
				return count
			if gameState == GameStatus.FINISH:
				dead = True
			if numMove > dungeon.x * dungeon.x:
				return 100
			numMove += 1
		count += 1
	return count

# Get the number of attempt before a win for all instances for each algorithm
def benchNumTryBeforeWin(numTry, maxLife, numEpisode):
	dungeons = getDungeons()
	countGurobi = dict()
	countIteVal = dict()
	countQLearn = dict()
	numDungeon = 1
	for dungeon in dungeons:
		print("Bench " + dungeon.name + ", dungeon " + str(numDungeon) + " out of " + str(len(dungeons)))
		g = Graphics(800, 1000, dungeon, 5, maxLife, maxLife)
		countGurobi[dungeon] = 0.0
		countIteVal[dungeon] = 0.0
		# countQLearn[dungeon] = 0.0
		for i in range(numTry):
			countGurobi[dungeon] = countGurobi[dungeon] + getNumTryBeforWinPDM(dungeon, g, True, False, maxLife, numEpisode)
			countIteVal[dungeon] = countIteVal[dungeon] + getNumTryBeforWinPDM(dungeon, g, False, False, maxLife, numEpisode)
			# countQLearn[dungeon] = countQLearn[dungeon] + getNumTryBeforWinPDM(dungeon, g, False, True, maxLife, numEpisode)
		countGurobi[dungeon] = countGurobi[dungeon] / numTry
		countIteVal[dungeon] = countIteVal[dungeon] / numTry
		# countQLearn[dungeon] = countQLearn[dungeon] / numTry
		numDungeon += 1
	return (countIteVal, countGurobi, countQLearn)

# Plot the solve timing
def plotNumTryBeforeWin(maxSize, numTry, numInstBySize, maxLife, numEpisode):
	print("Benching attempts")
	(countIteVal, countGurobi, countQLearn) = benchNumTryBeforeWin(numTry, maxLife, numEpisode)
	meanBySizeIteVal = []
	meanBySizeGurobi = []
	meanBySizeQLearn = []
	for i in range(maxSize - 2):
		meanBySizeGurobi.append(0)
		meanBySizeIteVal.append(0)
		# meanBySizeQLearn.append(0)
	for (k, val) in countIteVal.items():
		meanBySizeIteVal[k.x - 2] = meanBySizeIteVal[k.x - 2] + val
	for (k, val) in countGurobi.items():
		meanBySizeGurobi[k.x - 2] = meanBySizeGurobi[k.x - 2] + val
	# for (k, val) in countQLearn.items():
	# 	meanBySizeQLearn[k.x - 2] = meanBySizeQLearn[k.x - 2] + val
	for i in range(maxSize - 2):
		meanBySizeGurobi[i] = meanBySizeGurobi[i] / numInstBySize
		meanBySizeIteVal[i] = meanBySizeIteVal[i] / numInstBySize
		# meanBySizeQLearn[i] = meanBySizeQLearn[i] / numInstBySize

	file = open("DataNbAttempts", "w")
	file.write(str(meanBySizeGurobi) + "\n")
	file.write(str(meanBySizeIteVal) + "\n")
	# file.write(str(meanBySizeQLearn) + "\n")
	file.close()

	plt.close('all')
	plt.figure()
	plt.plot(range(2, maxSize, 1), meanBySizeGurobi, label = "PDM Gurobi")
	plt.plot(range(2, maxSize, 1), meanBySizeIteVal, label = "PDM IteVal")
	# plt.plot(range(2, maxSize, 1), meanBySizeQLearn, label = "Q-Learning")
	plt.legend(loc = 0)
	plt.suptitle("Number of attempts before winning for each algorithm")
	plt.xlabel('Dungeon size')
	plt.ylabel('Mean number of attempts')
	plt.savefig("../Plot/PlotNumAttemps.png", dpi = 200)

# Get the num of iteration all instances for each algorithm
def benchNumIte(numTry, maxLife):
	dungeons = getDungeons()
	numItes = dict()
	numDungeon = 1
	for dungeon in dungeons:
		print("Bench dungeon " + str(numDungeon) + " out of " + str(len(dungeons)))
		g = Graphics(800, 1000, dungeon, 5, maxLife, maxLife)
		p = Player(dungeon.x - 1, dungeon.y - 1, maxLife, g)
		pdm = PDM(dungeon, maxLife)
		numItes[dungeon] = iteration_algo(dungeon, pdm, 1, 1, True)
		numItes[dungeon] = numItes[dungeon]
		numDungeon += 1
	return numItes

# Plot the solve timing
def plotNumIte(maxSize, numTry, numInstBySize, maxLife):
	print("Benching NumIte")
	numIte = benchNumIte(numTry, maxLife)
	meanBySizeIteVal = []
	for i in range(maxSize - 2):
		meanBySizeIteVal.append(0)
	for (k, val) in numIte.items():
		meanBySizeIteVal[k.x - 2] = meanBySizeIteVal[k.x - 2] + val
	for i in range(maxSize - 2):
		meanBySizeIteVal[i] = meanBySizeIteVal[i] / numInstBySize

	file = open("DataNumIte", "w")
	file.write(str(meanBySizeIteVal) + "\n")
	file.close()

	plt.close('all')
	plt.figure()
	plt.plot(range(2, maxSize, 1), meanBySizeIteVal, label = "PDM IteVal")
	plt.legend(loc = 0)
	plt.suptitle("Number of iterations for iteration value algorithm")
	plt.xlabel('Dungeon size')
	plt.ylabel('Mean number of iteration')
	plt.savefig("../Plot/PlotNumIte.png", dpi = 200)

# Run the benches
def bench():
	numInstBySize = 11
	maxSizeTime = 16
	maxSizeAttemps = 16
	numTry = 11
	maxLife = 1
	numEpisode = 10000
	print("==== Benching ====")
	# generateDungeons(numInstBySize, max(maxSizeAttemps, maxSizeTime))
	# plotSolveTime(maxSizeTime, numTry, numInstBySize, maxLife)
	# plotNumTryBeforeWin(maxSizeAttemps, numTry, numInstBySize, maxLife, numEpisode)
	plotNumIte(maxSizeAttemps, numTry, numInstBySize, maxLife)