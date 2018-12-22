from player import Movement
from state import State
import random

# Class for a PDM used for Q-learning also defined as a set of nodes
class learningPDM:
    # Class for the nodes of Q-PDM defined by a state, a learning parameter, and the possible actions and their values
    class Node:
        def __init__(self, state, dungeon, learningRate):
            self.state = state
            self.learningRate = learningRate
            self.dungeon = dungeon
            self.action = dict()            # dict(float), keys are actions and value the value gained from the action
            # Initializes the actions: if we are not the dead state, we have actions
            if (self.state.pos[0] != -9 and self.state.pos[1] != -9):
                for move in [Movement.LEFT, Movement.RIGHT, Movement.TOP, Movement.DOWN]:
                    if not dungeon.is_wall(self.state.pos[0] + move.value[0], self.state.pos[1] + move.value[1]):
                    	# Initial value of a node is 0
                        self.action[move] = 0.0

        def __repr__(self):
            return str(self.action) 

        # Add an observation and update the value of the nodes accordingly
        def addObservation(self, move, newState, newNode):
            bestAction = newNode.getMaxAction()
            if bestAction != None:
                self.action[move] = (1 - self.learningRate) * self.action[move] + \
                self.learningRate * (newState.evaluate(self.dungeon) + bestAction[1])
            else:
                self.action[move] = (1 - self.learningRate) * self.action[move] + \
                self.learningRate * newState.evaluate(self.dungeon)

        # Returns the best actions in the node and its value
        def getMaxAction(self):
            disp = self.state.pos[0] == 0 and self.state.pos[1] == 1
            maxVal = -10000.0
            for (move, val) in self.action.items():
                if val >= maxVal:
                    maxVal = val
                    bestAction = move
            return (bestAction, maxVal) if maxVal != -10000.0 else None

    # Initializes a PDM by creating all the nodes plus the dead node
    def __init__(self, dungeon, learningRate):
        self.lastMove = None
        self.dungeon = dungeon
        self.nodes = dict()
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j):
                    for t in [True, False]:
                        for k in [True, False]:
                            for s in [True, False]:
                                state = State(t, k, s, (i, j))
                                self.nodes[state] = self.Node(state, dungeon, learningRate)
        # Plus the dead state (-9, -9)
        i = -9
        j = -9
        for t in [True, False]:
            for k in [True, False]:
                for s in [True, False]:
                    state = State(t, k, s, (i, j))
                    self.nodes[state] = self.Node(state, dungeon, learningRate)
        
    # Add an observation and update the value of the node concerned accordingly
    def addObservation(self, previousState, currentState):
        self.nodes[previousState].addObservation(self.lastMove, currentState, self.nodes[currentState])

    # Returns the move to play in a current state by selecting the best action
    def get_next_move(self, state):
        self.lastMove = self.nodes[state].getMaxAction()[0]
        return self.lastMove