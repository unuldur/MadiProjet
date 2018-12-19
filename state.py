class State:

    def __init__(self, treasure, key, sword, pos, *dead):
        self.treasure = treasure
        self.key = key
        self.sword = sword
        self.pos = pos
        if dead is None:
            self.dead = False
        else:
            self.dead = dead

    def __str__(self):
        return str(self.pos) + ", " + str(self.key) + ", " + str(self.treasure) + ", " + str(self.sword)

    def __repr__(self) -> str:
        return '(' + str(self.pos) + ", " + str(self.key) + ", " + str(self.treasure) \
               + ", " + str(self.sword) + ", " + str(self.dead) + ')'

    def __eq__(self, other):
        return self.treasure == other.treasure and self.key == other.key and self.sword == other.sword \
               and self.pos == other.pos and self.dead == other.dead

    def __hash__(self) -> int:
        return 2 * hash(self.pos) + 4 * hash(self.sword) + 8 * hash(self.treasure) + 16 * hash(self.key) \
               + 32 * hash(self.dead)

    def evaluate(self, dungeon):
        if self.pos[0] == dungeon.x - 1 and self.pos[1] == dungeon.y - 1 and self.treasure:
            return 1000000
        # The adventurer is dead
        elif self.pos == (-9, -9):
            return -100000
        return -1