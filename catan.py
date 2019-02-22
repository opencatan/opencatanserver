from enum import Enum
from graph import Vertex, Graph
import networkx as nx
from classes import Turn, Settlement, Resource
from tile import Tile, generate_board
from player import Player
from vertex import Vertex
import sys
from robber import Robber

class Catan:
    def __init__(self, tiles, players):
        self.tiles = tiles #2d array
        self.make_graph()

        self.players = [Player(name) for name in players]

        #test values
        self.players[0].resources['ore'] = 2
        self.players[1].resources['wheat'] = 2
        self.robber = Robber(1, 1)

        self.turn = self.players[0]
        self.phase = 0
        self.bank = {Resource.WHEAT: 20, Resource.ORE: 20, Resource.SHEEP: 20, Resource.BRICK: 20, Resource.WOOD: 20} #todo: custom bank. check these numbers

    def generate(self, top_width, middle_width):
        self.tiles = generate_board(top_width, middle_width)

    def make_graph(self):
        #create graph
        self.graph = nx.Graph()

        #create vertices
        for i, row in enumerate(self.tiles):
            offset = 0 if i % 2 == 1 else -1 #odd rows are inset 1/2
            for j, tile in enumerate(row):
                if tile is None:
                    continue
                v0 = v1 = v2 = v3 = v4 = v5 = None

                # get above left tile
                #todo: dont use raise/except
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
                for k, v in enumerate([v0, v1, v2, v3, v4, v5]):
                    if v is None:
                        v = Vertex()
                        v.location = (i, j, k)
                        self.graph.add_node(v)
                    tile.vertices.append(v)

        #connect vertices
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    continue
                for i, vertex in enumerate(tile.vertices):
                    v2 = tile.vertices[i-1]
                    self.graph.add_edge(vertex, v2)
                    #graph.connect(vertex, v2, 1)

#  **************** Accessor methods ****************

    def player_with_name(self, name):
        try:
            return [player for player in self.players if player.name == name][0]
        except IndexError:
            return None

#  **************** Placement methods ****************

    def place_road(self, v1, v2, player):
        #todo: adjacency check and other error handling

        self.graph[v1][v2]['owner'] = player
        self.graph[v1][v2]['type'] = 'road'

        return True, None

    def place_settlement(self, vertex, player, must_connect_to_road=True):
        #check that there is no adjacent settlement
        for neighbor in self.graph.neighbors(vertex):
            if neighbor.settlement is not None:
                return False, "You can't place a settlement adjacent to another settlement"

        if must_connect_to_road:
            connected = False
            for _, _, edge_data in self.graph.edges(vertex, data=True):
                if 'owner' in edge_data and edge_data['owner'] == player:
                    connected = True
            if not connected:
                return False, "You must place a settlement connected to a road"

        #success
        vertex.settlement = Settlement.SETTLEMENT
        vertex.owner = player
        return True, None

    def place_city(self, vertex, player):
        if vertex.owner != player:
            return False, "You must own this settlement to upgrade it to a city"

        if vertex.settlement != Settlement.SETTLEMENT:
            return False, "You must build a settlement before you can build a city"

        #success
        vertex.settlement = Settlement.CITY
        return True, None


    def serialized_settlements(self):
        return [vertex.serialize() for vertex in self.graph.nodes if vertex is not None and vertex.settlement is not None]

    def serialized_roads(self):
        #get all edges
        edges = [(v1, v2, data) for v1, v2, data in self.graph.edges(data=True) if data]
        #get locations out of vertices and name out of owner
        edges = [(v1.location, v2.location, {key: value.name if key == 'owner' else value for key, value in data.items()}) for v1, v2, data in edges]
        return edges
