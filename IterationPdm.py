from cell import Cell
from state import State
from gurobipy import *

class BellmanEquation:
    def __init__(self, cell, ug, nodes, gamma):
        self.cell = cell
        self.ug = ug
        self.nodes = nodes
        self.gamma = gamma

    def next_value(self, nodes_value, dungeon):
        val_max = -100
        index = None
        for k in self.cell.action.keys():
            new_state = State(self.cell.state.treasure, self.cell.state.key, self.cell.state.sword,
                  (self.cell.state.pos[0] + k[0], self.cell.state.pos[1] + k[1]))
            val = new_state.evaluate(dungeon) - 1
            for (p, ns) in self.cell.action[k]:
                val += self.gamma * p * nodes_value[ns]
            if val > val_max:
                val_max = val
                index = new_state
        if index is not None:
            return val_max, index
        return self.ug, None

    def get_contraints(self, variables, dungeon):
        contraints = []
        for k in self.cell.action.keys():
            new_state = State(self.cell.state.treasure, self.cell.state.key, self.cell.state.sword,
                              (self.cell.state.pos[0] + k[0], self.cell.state.pos[1] + k[1]))
            ctr = LinExpr()
            ctr += new_state.evaluate(dungeon) - 1
            for (p, ns) in self.cell.action[k]:
                ctr += self.gamma * p * variables[ns]
            contraints.append(ctr)
        return contraints


def iteration_algo(dungeon, pdm, gamma, e):
    bellmans = dict()
    nodes_value = dict()
    for s in pdm.nodes.keys():
        bellmans[s] = BellmanEquation(pdm.nodes[s], s.evaluate(dungeon), pdm.nodes, gamma)
        nodes_value[s] = 0
    use = dict()
    last = None
    for i in range(100):
        new_nodes_value = dict()
        for s in bellmans.keys():
            v, ns = bellmans[s].next_value(nodes_value, dungeon)
            new_nodes_value[s] = v
            use[s] = ns
        last = nodes_value
        nodes_value = new_nodes_value
        print(nodes_value)
    return use, nodes_value


def pl_algo(dungeon, pdm, gamma):
    model = Model("PDM solver")
    variables = dict()
    bellmans = []
    obj = LinExpr()
    for s in pdm.nodes.keys():
        v = model.addVar(vtype=GRB.CONTINUOUS, name=str(s))
        obj += v
        variables[s] = v
        bellmans.append((BellmanEquation(pdm.nodes[s], s.evaluate(dungeon), pdm.nodes, gamma), s))
    model.setObjective(obj, GRB.MINIMIZE)
    for (b, s) in bellmans:
        contraints = b.get_contraints(variables, dungeon)
        for c in contraints:
            model.addConstr(variables[s] >= c)
    model.optimize()
    node_value = dict()
    for v in model.getVars():
        state = None
        for k in variables.keys():
            if v.varName == variables[k].varName:
                state = k
                break
        node_value[state] = v.x

    use = dict()
    for (b, s) in bellmans:
        _, n = b.next_value(node_value, dungeon)
        use[s] = n
    return use, node_value



