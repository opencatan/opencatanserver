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
        #create graph
        self.graph = nx.Graph()

        count = 0
        #create vertices
        for i, row in enumerate(self.tiles):
            offset = 0 if i % 2 == 1 else -1 #odd rows are inset 1/2
            for j, tile in enumerate(row):
                if tile is None:
                    continue
                v0 = v1 = v2 = v3 = v4 = v5 = None

                # get above left tile
                try:
                    x, y = i-1, j+offset
                    if x < 0 or y < 0:
                        raise IndexError
                    above_left = self.tiles[x][y]
                except IndexError:
                    above_left = None

                # get above right tile
                try:
                    x, y = i-1, j+offset+1
                    if x < 0 or y < 0:
                        raise IndexError
                    above_right = self.tiles[x][y]
                except IndexError:
                    above_right = None

                # get left tile
                try:
                    x, y = i, j-1
                    if x < 0 or y < 0:
                        raise IndexError
                    left = self.tiles[x][y]
                except IndexError:
                    left = None

                #get what we can out of each of them, we may have redundancies
                # get vertices
                if above_left is not None:
                    v0 = above_left.vertices[4]
                    v1 = above_left.vertices[3]
                if above_right is not None:
                    v1 = above_right.vertices[5]
                    v2 = above_right.vertices[4]
                if left is not None:
                    v0 = left.vertices[2]
                    v5 = left.vertices[3]

                # add new vertices
                if v0 is None:
                    v0 = count
                    self.graph.add_node(count, has=[])
                    count += 1
                if v1 is None:
                    v1 = count
                    self.graph.add_node(count, has=[])
                    count += 1
                if v2 is None:
                    v2 = count
                    self.graph.add_node(count, has=[])
                    count += 1
                if v3 is None:
                    v3 = count
                    self.graph.add_node(count, has=[])
                    count += 1
                if v4 is None:
                    v4 = count
                    self.graph.add_node(count, has=[])
                    count += 1
                if v5 is None:
                    v5 = count
                    self.graph.add_node(count, has=[])
                    count += 1

                tile.vertices = [v0, v1, v2, v3, v4, v5] 

        #connect vertices
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    continue
                for i, vertex in enumerate(tile.vertices):
                    v2 = tile.vertices[i-1]
                    self.graph.add_edge(vertex, v2) 
                    #graph.connect(vertex, v2, 1)

    def place_settlement(self, vertex, player):
        attrs = {vertex: {'has': ['settlement', player]}}
        nx.set_node_attributes(self.graph, attrs)

    # This doesnt work yet. testing with test.py
    def place_city(self, vertex, player):
        print ("checking... " + str(self.graph.nodes[vertex]['has']))
        if 'settlement' is not in self.graph.nodes[vertex]['has'] or name is not in self.graph.nodes[vertex]['has']:
            print ('you done fucked up now. you cant build that!')
        else:
            attrs = {vertex: {'has': ['city', player]}}
            nx.set_node_attributes(self.graph, attrs)
