from enum import Enum


class Etat(Enum):
    MOVE = 1
    DEAD = 2
    STAY = 3
    GET_KEY = 4
    GET_SWORD = 5
    GET_TREASURE = 7
    WIN = 6
    KILL_ENEMY = 8
