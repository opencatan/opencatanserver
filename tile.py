from classes import Resource
import sys
from random import choice, randrange

def generate_random_tiles(n):
    return [Tile(choice(list(Resource)), randrange(2,12)) for x in range(n)]

def generate_board(top_width, middle_width):
    assert middle_width % 2
    board = []
    height = (middle_width - top_width) * 2 + 1
    array_width = height + 1
    for j in range(height):
        new_row = []
        for i in range(middle_width):
            new_row.append(None)
        board.append(new_row)

    for n, i in enumerate(range(top_width, middle_width+1)):
        tiles = generate_random_tiles(i)
        if not n % 2: # even rows
            start_pos = (middle_width - (i))//2
            board[n][start_pos:middle_width-start_pos] = tiles
        if n % 2:
            board[n][start_pos-1:middle_width-start_pos] = tiles

    for n, i in enumerate(range(top_width, middle_width)):
        tiles = generate_random_tiles(i)
        if not n % 2: # even rows
            start_pos = (middle_width - (i))//2
            board[-n-1][start_pos:middle_width-start_pos] = tiles
        if n % 2:
            board[-n-1][start_pos-1:middle_width-start_pos] = tiles
    return board
 
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
        if row_offset:
            index_tiles_start += 1

        top_row = [None] * index_tiles_start +\
                        generate_random_tiles(num_tiles_in_row) + \
                        [None] * index_tiles_start 

        bottom_row = [None] * index_tiles_start + \
                        generate_random_tiles(num_tiles_in_row) + \
                        [None] * index_tiles_start 

        board.insert(0, top_row)
        board.append(bottom_row)
        row_offset = not row_offset
    print(board)
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
