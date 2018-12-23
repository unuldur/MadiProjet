from dungeon import *
from player import Player
from pdm import PDM
from solverPDM import *
from time import time
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt

# Generate a set of instance of dungeon
def generateDungeons(numInstBySize, maxSize):
	dungeonFiles = [f for f in listdir("../Dungeons") if isfile(join("../Dungeons/", f))]
	for f in dungeonFiles:
		os.unlink("../Dungeons/" + f)
	for i in range(2, maxSize):
		for j in range(numInstBySize):
			d = random_dungeon_generation(i, i)
			d.write("../Dungeons/D_" + str(i) + "_" + str(i) + "_num_" + str(j))

def getDungeons():
	dungeonFiles = [f for f in listdir("../Dungeons") if isfile(join("../Dungeons/", f))]
	dungeons = []
	for d in dungeonFiles:
		dungeons.append(load_dungeon(join("../Dungeons/", d)))
	return dungeons

def getSolveTime(dungeon, gurobi):
    p = Player(dungeon.x - 1, dungeon.y - 1)
    pdm = PDM(dungeon)
    startTime = time()
    # Compute the policy using iteration value algorithm or integer programming
    if gurobi:
        strat, value = pl_algo(dungeon, pdm, 0.9)
    else:
        strat, value = iteration_algo(dungeon, pdm, 1, 1)
    return time() - startTime

def benchSolveTime(numTry):
	dungeons = getDungeons()
	timeGurobi = dict()
	timeIteVal = dict()
	for dungeon in dungeons:
		timeGurobi[dungeon] = 0.0
		timeIteVal[dungeon] = 0.0
		for i in range(numTry):
			timeGurobi[dungeon] = timeGurobi[dungeon] + getSolveTime(dungeon, True)
			timeIteVal[dungeon] = timeIteVal[dungeon] + getSolveTime(dungeon, False)
		timeGurobi[dungeon] = timeGurobi[dungeon] / numTry
		timeIteVal[dungeon] = timeIteVal[dungeon] / numTry
	return (timeIteVal, timeGurobi)

def plotSolveTime(maxSize, numTry):
	(timeIteVal, timeGurobi) = benchSolveTime(numTry)
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
		meanBySizeGurobi[i] = meanBySizeGurobi[i] / numTry
		meanBySizeIteVal[i] = meanBySizeIteVal[i] / numTry

	print(list(range(2, maxSize, 1)))
	print(meanBySizeGurobi)
	print(meanBySizeIteVal)
	plt.close('all')
	plt.figure()
	plt.plot(range(2, maxSize, 1), meanBySizeGurobi, label = "PDM Gurobi")
	plt.plot(range(2, maxSize, 1), meanBySizeIteVal, label = "PDM IteVal")
	plt.legend(loc=0)
	plt.show()

def bench():
	numInstBySize = 1
	maxSize = 20
	numTry = 1
	generateDungeons(numInstBySize, maxSize)
	plotSolveTime(maxSize, numTry)