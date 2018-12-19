from final_node import FinalNode
from gameState import GameState
from state import State
from cell import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class PDM:
    class Cell:
        def __init__(self, dungeon, state):
            self.state = state
            self.action = dict()
            for (i, j) in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                if dungeon.is_wall(state.pos[0] + i, state.pos[1] + j):
                    continue
                new_state = State(state.treasure, state.key, state.sword, (state.pos[0] + i, state.pos[1] + j))
                self.action[(i, j)] = self.get_transition(dungeon, new_state)

        def get_transition(self, dungeon, state):
            m = dict()
            self.get_transition_matrice(dungeon, state, m)
            if len(m.keys()) == 1:
                tr = []
                for new_etat in cell_movement(dungeon.dungeon[state.pos], dungeon, state):
                    new_state = state
                    if new_etat[1] == Etat.MOVE:
                        new_state = State(state.treasure, state.key, state.sword, new_etat[2])
                    if new_etat[1] == Etat.DEAD:
                        new_state = State(state.treasure, state.key, state.sword, (-9, -9))
                    tr.append((new_etat[0], new_state))
                return tr
            transition = self.dict_to_transition(m)
            pi = np.zeros((1, len(m.keys())))
            i = 0
            for k in m.keys():
                if k == state:
                    pi[0, i] = 1
                i += 1
            next_pi = np.dot(pi, transition)
            while not np.allclose(next_pi, pi):
                pi = next_pi
                next_pi = np.dot(pi, transition)

            proba = []
            i = 0
            for k in m.keys():
                if pi[0, i] >= 0.0001:
                    proba.append((pi[0, i], k))
                i += 1
            return proba

        def get_transition_matrice(self, dungeon, state, m):
            m[state] = dict()
            if state.pos == (-9, -9):
                m[state][state] = 1
                return
            for new_etat in cell_movement(dungeon.dungeon[state.pos], dungeon, state):
                if new_etat[1] == Etat.STAY or new_etat[1] == Etat.KILL_ENEMY:
                    m[state][state] = 1
                    return
                new_state = state
                if new_etat[1] == Etat.MOVE:
                    new_state = State(state.treasure, state.key, state.sword, new_etat[2])
                if new_etat[1] == Etat.GET_KEY:
                    new_state = State(state.treasure, True, state.sword, state.pos)
                if new_etat[1] == Etat.GET_SWORD:
                    new_state = State(state.treasure, state.key, True, state.pos)
                if new_etat[1] == Etat.GET_TREASURE:
                    new_state = State(True, state.key, state.sword, state.pos)
                if new_etat[1] == Etat.DEAD:
                    new_state = State(state.treasure, state.key, state.sword, (-9, -9))
                if new_state not in m.keys():
                    self.get_transition_matrice(dungeon, new_state, m)
                m[state][new_state] = new_etat[0]

        def dict_to_transition(self, m):
            size = len(m.keys())
            transition = np.zeros((size, size))
            i = 0
            for k1 in m.keys():
                j = 0
                for k2 in m.keys():
                    if k2 in m[k1].keys():
                        transition[i, j] = m[k1][k2]
                    j += 1
                i += 1
            return transition

    def __init__(self, dungeon):
        self.nodes = dict()
        state = State(False, False, False, (dungeon.x - 1, dungeon. y - 1))
        note_to_do = self.next_nodes(dungeon, state)
        while len(note_to_do) > 0:
            next_node = note_to_do.pop()
            note_to_do.extend(self.next_nodes(dungeon, next_node))

    def next_nodes(self, dungeon, state):
        c = self.Cell(dungeon, state)
        self.nodes[state] = c
        next_nodes = []
        for k in c.action.keys():
            for (_, other_state) in c.action[k]:
                if other_state not in self.nodes.keys() and other_state not in next_nodes:
                    next_nodes.append(other_state)
        return next_nodes
