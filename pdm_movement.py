from movement import Movement

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
