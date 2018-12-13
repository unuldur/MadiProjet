from action_node import ActionNode, ProbaNode
from final_node import FinalNode
from gameState import GameState
from state import State
from cell import *
import networkx as nx
import matplotlib.pyplot as plt


class PDM:
    class Cell:
        def __init__(self, dungeon, state):
            self.transition = []
            for new_etat in cell_movement(dungeon.dungeon[state.pos], dungeon, state):
                game_state = GameState.NONE
                new_state = state
                if new_etat[1] == Etat.MOVE:
                    new_state = State(state.treasure, state.key, state.sword, new_etat[2])
                if new_etat[1] == Etat.GET_KEY:
                    new_state = State(state.treasure, True, state.sword, state.pos)
                if new_etat[1] == Etat.GET_SWORD:
                    new_state = State(state.treasure, state.key, True, state.pos)
                if new_etat[1] == Etat.GET_TREASURE:
                    new_state = State(True, state.key, state.sword, state.pos)
                if new_etat[1] == Etat.WIN:
                    game_state = GameState.WIN
                if new_etat[1] == Etat.DEAD:
                    game_state = GameState.DEAD
                    new_state = State(state.treasure, state.key, state.sword, (-1, -1))
                self.transition.append((new_etat[0], game_state, new_state))

    def __init__(self, dungeon):
        self.nodes = dict()
        state = State(False, False, False, (dungeon.x - 1, dungeon.y - 1))
        next_states = [state]
        while len(next_states) > 0:
            state = next_states.pop()
            cell = self.Cell(dungeon, state)
            self.nodes[state] = cell
            for (_, gs, ns) in cell.transition:
                if gs == GameState.NONE and ns not in self.nodes.keys():
                    next_states.append(ns)
                if gs == GameState.DEAD or gs == GameState.WIN:
                    self.nodes[ns] = None
            for (i, j) in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                next_state = State(state.treasure, state.key, state.sword, (state.pos[0] + i, state.pos[1] + j))
                if not dungeon.is_wall(state.pos[0] + i, state.pos[1] + j) and next_state not in self.nodes.keys():
                    next_states.append(next_state)

    def print(self):
        g = nx.Graph()
        for k in self.nodes.keys():
            k = self.nodes[k]
            if isinstance(k, ActionNode):
                if k.left is not None:
                    g.add_edge(str(k.id), str(k.left.id))
                if k.right is not None:
                    g.add_edge(str(k.id), str(k.right.id))
                if k.up is not None:
                    g.add_edge(str(k.id), str(k.up.id))
                if k.down is not None:
                    g.add_edge(str(k.id), str(k.down.id))
            if isinstance(k, ProbaNode):
                for (_, node) in k.transition:
                    g.add_edge(str(k.id), str(node.id))
        nx.draw(g)
        plt.savefig("simple_path.png")
        plt.show()
