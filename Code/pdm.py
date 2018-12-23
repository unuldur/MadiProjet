from player import Movement, get_next_game_state
from state import State
import numpy as np

# Class for a PDM defined by a set of nodes stored as a dictionary where keys are state
class PDM:
    # Class for the Node of a PDM identified by a state and containing the possible actions of the node
    class Node:
        def __init__(self, state, dungeon, isFinal):
            self.state = state
            self.action = dict()        # Dict(List(Couple(Proba, state))), keys are movement
            self.isFinal = isFinal
            
            # Initializes the actions: if we are not the dead state, we have actions
            if (self.state.pos[0] != -9 and self.state.pos[1] != -9):
                for move in [Movement.LEFT, Movement.RIGHT, Movement.TOP, Movement.DOWN]:
                    if not dungeon.is_wall(self.state.pos[0] + move.value[0], self.state.pos[1] + move.value[1]):
                        nextCellPos = (self.state.pos[0] + move.value[0], self.state.pos[1] + move.value[1])
                        nextCell = dungeon.cells[nextCellPos]
                        self.action[move] = get_next_game_state(nextCell, nextCellPos, dungeon, self.state)

    # Initializes a PDM by creating all the nodes plus the dead node
    def __init__(self, dungeon):
        self.nodes = dict()
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j):
                    for t in [True, False]:
                        for k in [True, False]:
                            for s in [True, False]:
                                state = State(t, k, s, (i, j))
                                if (state.pos == (dungeon.x - 1, dungeon.y - 1) and t):
                                    self.nodes[state] = self.Node(state, dungeon, True)
                                else:
                                    self.nodes[state] = self.Node(state, dungeon, False)
        # Plus the dead state (-9, -9)
        i = -9
        j = -9
        for t in [True, False]:
            for k in [True, False]:
                for s in [True, False]:
                    state = State(t, k, s, (i, j))
                    self.nodes[state] = self.Node(state, dungeon, True)

# Class to store a policy
class PdmMovement:
    def __init__(self, policy):
        self.policy = policy

    # Returns the move played by the policy in the state state
    def get_next_move(self, state):
        action = self.policy[state]
        if action is None:
            return Movement.STOP
        else:
            return action