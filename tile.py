from classes import Resource
import sys

def normalize_half_index(index):
        if int(index) == index: # we are in a normal row
            return index
        else:
            return int(index+0.5) # we're in a wierd row, 0.5 -> 1st element of array, 1.5 -> 2nd element of array, etc...

class TileBoard:
    def __init__(self, board):
        self.board = []

class Tile:
    def __init__(self, resource_type, resource_number):
        if not isinstance(resource_type, Resource):
            print("resource param is not of type Resource", file=sys.stderr)
        self.resource_type = resource_type
        self.resource_number = resource_number
        self.has_robber = False
        self.vertices = []
