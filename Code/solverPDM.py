from state import State
from gurobipy import *
import time

# Class for the Bellman Equations of a given PDM node with ug the utility of the node, 
# nodes all the nodes of the PDM, and gamma the actualization rate
class BellmanEquation:
    def __init__(self, node, ug, nodes, gamma):
        self.node = node
        self.ug = ug
        self.nodes = nodes
        self.gamma = gamma

    # Compute the new value of the node given the current values
    def next_value(self, nodes_value, dungeon):
        if self.node.isFinal:
            return (self.ug, None)
        val_max = -1000000
        action = None
        for k in self.node.action.keys():
            val = -1
            for (proba, state) in self.node.action[k]:
                val += self.gamma * proba * nodes_value[state]
            if val > val_max:
                val_max = val
                action = k
        if action is not None:
            return (val_max, action)
        return (self.ug, None)

    # Generates the constraint for the integer program
    def get_contraints(self, variables, dungeon):
        contraints = []
        for k in self.node.action.keys():
            ctr = LinExpr()
            ctr += -1
            for (p, ns) in self.node.action[k]:
                ctr += self.gamma * p * variables[ns]
            contraints.append(ctr)
        return contraints

def stopIteVal(previousValues, currentValues):
    if previousValues == None or currentValues == None:
        return 1000000
    bestVal = -9000000
    for k in previousValues.keys():
        if bestVal < abs(previousValues[k] - currentValues[k]):
            bestVal = abs(previousValues[k] - currentValues[k])
    return bestVal

# Value iteration algorithm
def iteration_algo(dungeon, pdm, gamma, e):
    bellmans = dict()
    nodes_value = dict()
    # For each node of the PDM Bellman equations are initialized
    for s in pdm.nodes.keys():
        bellmans[s] = BellmanEquation(pdm.nodes[s], s.evaluate(dungeon), pdm.nodes, gamma)
        nodes_value[s] = 0
    policy = dict()
    last = None
    # While the stopping criteria is not met we udpate the node values given their current one and the bellman equations
    while stopIteVal(last, nodes_value) > e:
        new_nodes_value = dict()
        for s in bellmans.keys():
            val, action = bellmans[s].next_value(nodes_value, dungeon)
            new_nodes_value[s] = val
            policy[s] = action
        last = nodes_value
        nodes_value = new_nodes_value
    return policy, nodes_value

# PDM solver using integer programming
def pl_algo(dungeon, pdm, gamma):
    model = Model("PDM solver")
    variables = dict()
    bellmans = []
    obj = LinExpr()
    # Creates the objective functions and the Bellman equations
    for s in pdm.nodes.keys():
        v = model.addVar(vtype=GRB.CONTINUOUS, name=str(s))
        obj += v
        variables[s] = v
        bellmans.append((BellmanEquation(pdm.nodes[s], s.evaluate(dungeon), pdm.nodes, gamma), s))
    model.setObjective(obj, GRB.MINIMIZE)
    # Creates the constraints given the Bellman equations
    for (b, s) in bellmans:
        contraints = b.get_contraints(variables, dungeon)
        for c in contraints:
            model.addConstr(variables[s] >= c)
    # Solves the integer program and gets the state values
    model.optimize()
    node_value = dict()
    for v in model.getVars():
        state = None
        for k in variables.keys():
            if v.varName == variables[k].varName:
                state = k
                break
        node_value[state] = v.x

    # Returns the optimal policy
    policy = dict()
    for (b, s) in bellmans:
        _, action = b.next_value(node_value, dungeon)
        policy[s] = action
    return policy, node_value