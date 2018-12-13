from cell import *
from final_node import FinalNode
from state import State


class ActionNode:

    def __init__(self, state):
        self.id = state
        self.down = None
        self.up = None
        self.left = None
        self.right = None

    def generate(self, dungeon, state, nodes):
        for (i, j) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if dungeon.is_wall(state.pos[0] + i, state.pos[1] + j):
                continue
            new_pos = (state.pos[0] + i, state.pos[1] + j)
            new_state = State(state.treasure, state.key, state.sword, new_pos)
            exist = new_state in nodes.keys()
            if i == 1:
                if exist:
                    self.right = nodes[new_state]
                else:
                    self.right = ProbaNode(new_state)
                    nodes[new_state] = self.right
                    self.right.generate(cell_movement(dungeon.dungeon[new_pos], dungeon, new_state), dungeon, new_state, nodes)

            if i == -1:
                if exist:
                    self.left = nodes[new_state]
                else:
                    self.left = ProbaNode(new_state)
                    nodes[new_state] = self.left
                    self.left.generate(cell_movement(dungeon.dungeon[new_pos], dungeon, new_state), dungeon, new_state, nodes)
            if j == -1:
                if exist:
                    self.up = nodes[new_state]
                else:
                    nodes[new_state] = ProbaNode(new_state)
                    self.up = nodes[new_state]
                    self.up.generate(cell_movement(dungeon.dungeon[new_pos], dungeon, new_state), dungeon, new_state, nodes)
            if j == 1:
                if exist:
                    self.down = nodes[new_state]
                else:
                    nodes[new_state] = ProbaNode(new_state)
                    self.down = nodes[new_state]
                    self.down.generate(cell_movement(dungeon.dungeon[new_pos], dungeon, new_state), dungeon, new_state, nodes)


class ProbaNode:

    def __init__(self, state):
        self.id = state
        self.transition = []

    def generate(self, probabilite, dungeon, state, nodes):
        for new_etat in probabilite:
            next_node = None
            if new_etat[1] == Etat.MOVE:
                new_pos = new_etat[2]
                new_state = State(state.treasure, state.key, state.sword, new_pos)
                next_node = ProbaNode(new_state)
                next_node.generate(cell_movement(dungeon.dungeon[new_pos], dungeon, new_state),
                                      dungeon, state, nodes)
            if new_etat[1] == Etat.GET_KEY:
                new_state = State(state.treasure, True, state.sword, state.pos)
                next_node = ActionNode(new_state)
                next_node.generate(dungeon, new_state, nodes)
            if new_etat[1] == Etat.GET_SWORD:
                new_state = State(state.treasure, state.key, True, state.pos)
                next_node = ActionNode(new_state)
                next_node.generate(dungeon, new_state, nodes)
            if new_etat[1] == Etat.GET_TREASURE:
                new_state = State(True, state.key, state.sword, state.pos)
                next_node = ActionNode(new_state)
                next_node.generate(dungeon, new_state, nodes)
            if new_etat[1] == Etat.KILL_ENEMY or Etat.STAY == new_etat[1]:
                    next_node = ActionNode(state)
                    next_node.generate(dungeon, state, nodes)
            if new_etat[1] == Etat.WIN:
                next_node = FinalNode(state, 100)
            if new_etat[1] == Etat.DEAD:
                next_node = FinalNode(state, 0)
            self.transition.append((new_etat[0], next_node))