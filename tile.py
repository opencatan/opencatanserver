from classes import Resource
import sys
from random import choice, randrange

def generate_random_tiles(n):
    return [Tile(choice(list(Resource)), 7) for x in range(n)]

def generate_board(top_width, middle_width):
    board = []
    board.append(generate_random_tiles(middle_width))

    #will the middle row be offset?

    if (top_width-middle_width) % 2 == 0:
        middle_offset = False

    else:
        middle_offset = True

    row_offset = not middle_offset
    index_tiles_start = 0
    for i in range(middle_width- top_width):
        num_tiles_in_row = middle_width - 1 - i 
        if not row_offset:
            index_tiles_start += 1

        top_row = [None] * index_tiles_start +\
                        generate_random_tiles(num_tiles_in_row) + \
                        [None] * index_tiles_start 

        bottom_row = [None] * index_tiles_start + \
                        generate_random_tiles(num_tiles_in_row) + \
                        [None] * index_tiles_start 

        if row_offset:
            top_row.append(None)
            bottom_row.append(None)

        board.insert(0, top_row)
        board.append(bottom_row)
        row_offset = not row_offset
    return board
        


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
