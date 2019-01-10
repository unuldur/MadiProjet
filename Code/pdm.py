from player import Movement
from state import State
from dungeon import Cell
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
            cell = dungeon.cells[self.state.pos[0], self.state.pos[1]]
            if (self.state.life > 0 and cell != Cell.CRACKS and cell != Cell.PORTAL and cell != Cell.PLATFORM):
                for move in [Movement.LEFT, Movement.RIGHT, Movement.TOP, Movement.DOWN]:
                    if not dungeon.is_wall(self.state.pos[0] + move.value[0], self.state.pos[1] + move.value[1]):
                        nextCellPos = (self.state.pos[0] + move.value[0], self.state.pos[1] + move.value[1])
                        nextCell = dungeon.cells[nextCellPos]
                        self.action[move] = get_transitions(nextCell, nextCellPos, dungeon, self.state)

    # Initializes a PDM by creating all the nodes plus the dead node
    def __init__(self, dungeon, maxLife):
        self.nodes = dict()
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j):
                    for t in [True, False]:
                        for k in [True, False]:
                            for s in [True, False]:
                                for l in range(maxLife + 1):
                                    state = State(t, k, s, (i, j), l)
                                    if (state.pos == (dungeon.x - 1, dungeon.y - 1) and t):
                                        self.nodes[state] = self.Node(state, dungeon, True)
                                    else:
                                        self.nodes[state] = self.Node(state, dungeon, False)

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

# What are the next states (with their probabilities) if we move to cell at cellPos from state in dungeon.
def get_transitions(cell, cellPos, dungeon, state):
    if cell in [Cell.EMPTY, Cell.START]:
        return [(1, State(state.treasure, state.key, state.sword, cellPos, state.life))]
    elif cell == Cell.KEY:
        return [(1, State(state.treasure, True, state.sword, cellPos, state.life))]
    elif cell == Cell.SWORD:
        return [(1, State(state.treasure, state.key, True, cellPos, state.life))]
    elif cell == Cell.TREASURE and state.key:
        return [(1, State(True, state.key, state.sword, cellPos, state.life))]
    elif cell == Cell.TREASURE:
        return [(1, State(state.treasure, state.key, state.sword, cellPos, state.life))]
    elif cell == Cell.CRACKS:
        return [(1, State(state.treasure, state.key, state.sword, cellPos, 0))]
    elif cell == Cell.ENEMY and state.sword:
        return [(1, State(state.treasure, state.key, state.sword, cellPos, state.life))]
    elif cell == Cell.ENEMY:
        return [(0.7, State(state.treasure, state.key, state.sword, cellPos, state.life)), \
        (0.3, State(state.treasure, state.key, state.sword, cellPos, state.life - 1))] 
    elif cell == Cell.TRAP:
        return [(0.6, State(state.treasure, state.key, state.sword, cellPos, state.life)), \
        (0.1, State(state.treasure, state.key, state.sword, cellPos, state.life - 1)), \
        (0.3, State(state.treasure, state.key, state.sword, (dungeon.x - 1, dungeon.y - 1), state.life))]
    elif cell == Cell.PLATFORM:
        # Find all neightbours that are not walls
        possible_states = []
        for move in [Movement.LEFT, Movement.RIGHT, Movement.TOP, Movement.DOWN]:
            if not dungeon.is_wall(cellPos[0] + move.value[0], cellPos[1] + move.value[1]):
                possible_states.append(State(state.treasure, state.key, state.sword, 
                    (cellPos[0] + move.value[0], cellPos[1] + move.value[1]), state.life))
        res = []
        for s in possible_states:
            res.append((1 / len(possible_states), s))
        return res
    if cell == Cell.PORTAL:
        # Find all cells that are not walls
        possible_states = []
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if not dungeon.is_wall(i, j) and (i, j) != state.pos:
                    possible_states.append(State(state.treasure, state.key, state.sword, (i, j), state.life))
        res = []
        for s in possible_states:
            res.append((1 / len(possible_states), s))
        return res
    return []