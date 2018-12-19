from cell import Cell
from state import State


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

