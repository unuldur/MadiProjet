from cell import Cell
from state import State


class BellmanEquation:
    def __init__(self, states, ug, nodes, gamma):
        self.states = states
        self.ug = ug
        self.nodes = nodes
        self.gamma = gamma

    def next_value(self, nodes_value):
        val_max = -100
        index = -1
        i = 0
        for s in self.states:
            val = self.ug
            if self.nodes[s] is not None:
                for (p, _, ns) in self.nodes[s].transition:
                    val += self.gamma * p * nodes_value[ns]
            if val > val_max:
                val_max = val
                index = i
            i += 1
        if index >= 0:
            return val_max, self.states[index]
        return self.ug, None


def iteration_algo(dungeon, pdm, gamma, e):
    bellmans = dict()
    nodes_value = dict()
    for s in pdm.nodes.keys():

        states = []
        for (i, j) in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            x = s.pos[0] + i
            y = s.pos[1] + j
            if dungeon.is_wall(x, y):
                continue
            states.append(State(s.treasure, s.key, s.sword, (x, y)))
        bellmans[s] = BellmanEquation(states, s.evaluate(dungeon), pdm.nodes, gamma)
        nodes_value[s] = 0
    use = dict()
    last = None
    for i in range(100):
        new_nodes_value = dict()
        for s in bellmans.keys():
            v, ns = bellmans[s].next_value(nodes_value)
            new_nodes_value[s] = v
            use[s] = ns
        last = nodes_value
        nodes_value = new_nodes_value
        print(nodes_value)
    return use, nodes_value

