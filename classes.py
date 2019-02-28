from enum import Enum
import sys

class Turn(Enum):
    ROLLDICE = 0
    TRADE = 1
    BUILD = 2
    SP_BUILD = 3

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

    def excepted_resources():
        return [Resource.DESERT, Resource.WATER]
