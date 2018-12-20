from player import get_next_player_state, PlayerState, Movement, get_next_game_state
from state import State
import numpy as np

class PDM:
    class Node:
        def __init__(self, dungeon, state):
            self.state = state
            self.action = dict()
            for move in [Movement.LEFT, Movement.RIGHT, Movement.TOP, Movement.DOWN]:
                if dungeon.is_wall(state.pos[0] + move.value[0], state.pos[1] + move.value[1]):
                    continue
                new_state = State(state.treasure, state.key, state.sword, 
                    (state.pos[0] + move.value[0], state.pos[1] + move.value[1]))
                self.action[move.value] = self.get_transition(dungeon, new_state)

        # Returns List(Couple(Proba, State))
        def get_transition(self, dungeon, state):
            m = dict()
            self.get_transition_matrice(dungeon, state, m)
            if len(m.keys()) == 1:
                tr = []
                for transition in get_next_player_state(dungeon.cells[state.pos], dungeon, state):
                    new_state = state
                    if transition[1] == PlayerState.MOVE:
                        new_state = State(state.treasure, state.key, state.sword, transition[2])
                    if transition[1] == PlayerState.DEAD:
                        new_state = State(state.treasure, state.key, state.sword, (-9, -9))
                    tr.append((transition[0], new_state))
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
            for transition in get_next_player_state(dungeon.cells[state.pos], dungeon, state):
                if transition[1] == PlayerState.STAY or transition[1] == PlayerState.KILL_ENEMY:
                    m[state][state] = 1
                    return
                new_state = state
                if transition[1] == PlayerState.MOVE:
                    new_state = State(state.treasure, state.key, state.sword, transition[2])
                if transition[1] == PlayerState.GET_KEY:
                    new_state = State(state.treasure, True, state.sword, state.pos)
                if transition[1] == PlayerState.GET_SWORD:
                    new_state = State(state.treasure, state.key, True, state.pos)
                if transition[1] == PlayerState.GET_TREASURE:
                    new_state = State(True, state.key, state.sword, state.pos)
                if transition[1] == PlayerState.DEAD:
                    new_state = State(state.treasure, state.key, state.sword, (-9, -9))
                if new_state not in m.keys():
                    self.get_transition_matrice(dungeon, new_state, m)
                m[state][new_state] = transition[0]

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
        remainingNodes = self.next_nodes(dungeon, state)
        while len(remainingNodes) > 0:
            next_node = remainingNodes.pop()
            remainingNodes.extend(self.next_nodes(dungeon, next_node))

    def next_nodes(self, dungeon, state):
        c = self.Node(dungeon, state)
        self.nodes[state] = c
        next_nodes = []
        for k in c.action.keys():
            for (_, other_node) in c.action[k]:
                if other_node not in self.nodes.keys() and other_node not in next_nodes:
                    next_nodes.append(other_node)
        return next_nodes

class PDM2:
    class Node:
        def __init__(self, dungeon, state):
            self.state = state
            self.action = dict()        # Dict(List(Couple(Proba, state)))

        def setAction(self, dungeon):
            # If we are not the dead state we have actions
            if (self.state.pos[0] != -9 and self.state.pos[1] != -9):
                for move in [Movement.LEFT, Movement.RIGHT, Movement.TOP, Movement.DOWN]:
                    if not dungeon.is_wall(self.state.pos[0] + move.value[0], self.state.pos[1] + move.value[1]):
                        nextCellPos = self.state.pos[0] + move.value[0], self.state.pos[1] + move.value[1]
                        nextCell = dungeon.cells[nextCellPos]
                        self.action[move.value] = get_next_game_state(nextCell, nextCellPos, dungeon, self.state)
            
    def __init__(self, dungeon):
        self.nodes = dict()
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j):
                    for t in [True, False]:
                        for k in [True, False]:
                            for s in [True, False]:
                                state = State(t, k, s, (i, j))
                                self.nodes[state] = self.Node(dungeon, state)
        # Plus the dead state (-9, -9)
        i = -9
        j = -9
        for t in [True, False]:
            for k in [True, False]:
                for s in [True, False]:
                    state = State(t, k, s, (i, j))
                    self.nodes[state] = self.Node(dungeon, state)
        for (_, n) in self.nodes.items():
            n.setAction(dungeon)

class PdmMovement:
    def __init__(self, strat):
        self.strat = strat

    def get_next_move(self, state):
        new_pos = self.strat[state]
        if new_pos is None:
            return Movement.STOP
        difx = new_pos.pos[0] - state.pos[0]
        dify = new_pos.pos[1] - state.pos[1]
        if difx == 1:
            return Movement.RIGHT
        if difx == -1:
            return Movement.LEFT
        if dify == 1:
            return Movement.DOWN
        if dify == -1:
            return Movement.TOP
        return Movement.STOP