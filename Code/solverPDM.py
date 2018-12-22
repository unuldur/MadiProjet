from state import State
from gurobipy import *

# Class for the Bellman Equations of a given PDM node with ug the utility of the node, 
# nodes all the nodes of the PDM, and gamma the actualization rate
class BellmanEquation:
    def __init__(self, node, ug, nodes, gamma):
        self.node = node
        self.ug = ug
        self.nodes = nodes
        self.gamma = gamma

    # Compute the new value of the node give the current values
    def next_value(self, nodes_value, dungeon):
        val_max = -100
        index = None
        for k in self.node.action.keys():
            new_state = State(self.node.state.treasure, self.node.state.key, self.node.state.sword,
                  (self.node.state.pos[0] + k[0], self.node.state.pos[1] + k[1]))
            val = new_state.evaluate(dungeon) - 1
            for (p, ns) in self.node.action[k]:
                val += self.gamma * p * nodes_value[ns]
            if val > val_max:
                val_max = val
                index = new_state
        if index is not None:
            return val_max, index
        return self.ug, None

    # Generates the constraint for the integer program
    def get_contraints(self, variables, dungeon):
        contraints = []
        for k in self.node.action.keys():
            new_state = State(self.node.state.treasure, self.node.state.key, self.node.state.sword,
                              (self.node.state.pos[0] + k[0], self.node.state.pos[1] + k[1]))
            ctr = LinExpr()
            ctr += new_state.evaluate(dungeon) - 1
            for (p, ns) in self.node.action[k]:
                ctr += self.gamma * p * variables[ns]
            contraints.append(ctr)
        return contraints

# Value iteration algorithm
def iteration_algo(dungeon, pdm, gamma, e):
    bellmans = dict()
    nodes_value = dict()
    # For each node of the PDM Bellman equations are initialized
    for s in pdm.nodes.keys():
        bellmans[s] = BellmanEquation(pdm.nodes[s], s.evaluate(dungeon), pdm.nodes, gamma)
        nodes_value[s] = 0
    use = dict()
    last = None
    # While the stopping criteria is not met we udpate the node values given their current one and the bellman equations
    for i in range(10):
        new_nodes_value = dict()
        for s in bellmans.keys():
            v, ns = bellmans[s].next_value(nodes_value, dungeon)
            new_nodes_value[s] = v
            use[s] = ns
        last = nodes_value
        nodes_value = new_nodes_value
    return use, nodes_value

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
    use = dict()
    for (b, s) in bellmans:
        _, n = b.next_value(node_value, dungeon)
        use[s] = n
    return use, node_value