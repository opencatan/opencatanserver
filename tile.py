from classes import Resource
import sys
from random import choice

def generate_random_tiles(n):
    return [Tile(choice(list(Resource)), random.randrange(2,12)) for x in range(n)]

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
    print(board)

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
