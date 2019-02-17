from enum import Enum
import sys

class Turn(Enum):
    SP_PLACEMENT = 0
    ROLLDICE = 1
    TRADE = 2
    BUILD = 3
    SP_BUILD = 4

class Settlement(Enum):
    SETTLEMENT = 1
    CITY = 2

class Resource(Enum):
    WHEAT = "wheat"
    ORE = "ore"
    SHEEP = "sheep"
    BRICK = "brick"
    WOOD = "wood"
    DESERT = "desert"
    WATER = "water"
