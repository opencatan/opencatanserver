from enum import Enum
from graph import Vertex, Graph
import networkx as nx
from classes import Turn, Settlement, Resource
from tile import Tile
from player import Player
import sys
from robber import Robber

class Catan:
    def __init__(self, tiles, players):
        self.tiles = tiles #2d array
        self.make_graph()

        self.players = players #list of names
        self.robber = Robber(1, 1)
        self.turn = self.players[0]
        self.phase = 0
        self.bank = {Resource.WHEAT: 20, Resource.ORE: 20, Resource.SHEEP: 20, Resource.BRICK: 20, Resource.WOOD: 20} #todo: custom bank. check these numbers

    def make_graph(self):
        vertex_set = set()
        #create vertices
        for i, row in enumerate(self.tiles):
            offset = 0 if i % 2 == 1 else 0 #odd rows are inset 1/2
            for j, tile in enumerate(row):
                if tile is None:
                    continue
                v0 = v1 = v2 = v3 = v4 = v5 = None
                try:
                    x, y = i-1, j+offset
                    if x < 0 or y < 0:
                        raise IndexError
                    above_left = self.tiles[x][y]
                except IndexError:
                    above_left = None

                try:
                    x, y = i-1, j+offset+1
                    if x < 0 or y < 0:
                        raise IndexError
                    above_right = self.tiles[x][y]
                except IndexError:
                    above_right = None

                try:
                    x, y = i, j-1
                    if x < 0 or y < 0:
                        raise IndexError
                    left = self.tiles[x][y]
                except IndexError:
                    left = None

                #get what we can out of each of them, we may have redundancies
                if above_left is not None:
                    v0 = above_left.vertices[4]
                    v1 = above_left.vertices[3]
                if above_right is not None:
                    v1 = above_right.vertices[5]
                    v2 = above_right.vertices[4]
                if left is not None:
                    v0 = left.vertices[2]
                    v5 = left.vertices[3]

                tile.vertices = [v if v is not None else Vertex() for v in [v0, v1, v2, v3, v4, v5]]

                #untested (whoops)
                for vertex in tile.vertices:
                    vertex_set.add(vertex)
                    vertex.adjacent_tiles.append(tile) #circular reference (whoops)

        #create graph
        self.graph = Graph()
        for vertex in vertex_set:
            self.graph.insert(vertex)

        #connect vertices
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    continue
                for i, vertex in enumerate(tile.vertices):
                    v2 = tile.vertices[i-1]
                    self.graph.connect(vertex, v2, 1)

    def place_settlement(self, vertex, player):
        pass
