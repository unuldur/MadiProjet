# State of the game, defined by the player position and what he has picked
class State:
    def __init__(self, treasure, key, sword, pos):
        self.treasure = treasure
        self.key = key
        self.sword = sword
        self.pos = pos

    def __str__(self):
        return str(self.pos) + ", " + str(self.key) + ", " + str(self.treasure) + ", " + str(self.sword)

    def __repr__(self) -> str:
        return '(' + str(self.pos) + ", " + str(self.key) + ", " + str(self.treasure) + ", " + str(self.sword) + ')'

    def __eq__(self, other):
        return self.treasure == other.treasure and self.key == other.key and self.sword == other.sword \
               and self.pos == other.pos

    def __hash__(self) -> int:
        return 2 * hash(self.pos) + 4 * hash(self.sword) + 8 * hash(self.treasure) + 16 * hash(self.key)

    # Returns the evaluation of the state: 1000 if winnig position, -1000 if dead and -1 elsewhere
    def evaluate(self, dungeon):
        if self.pos[0] == dungeon.x - 1 and self.pos[1] == dungeon.y - 1 and self.treasure:
            return 1000000
        elif self.pos == (-9, -9):
            # Position (-9, -9) means the adventurer is dead
            return -1000
        return -1