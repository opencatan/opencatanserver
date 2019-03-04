from enum import Enum
from graph import Vertex, Graph
import networkx as nx
from classes import Turn, Settlement, Resource
from tile import Tile, generate_board
from player import Player
from vertex import Vertex
import sys
import random
from robber import Robber
from collections import defaultdict


class Catan:
    def __init__(self, tiles, players):
        self.tiles = tiles #2d array
        self.make_graph()

        self.players = [Player(name) for name in players]

        #test values
        #todo: actual game setup
        for player in self.players:
            for resource in Resource:
                    if resource not in Resource.excepted_resources():
                        player.resources[resource] = 3
        self.robber = Robber(1, 1)

        self.turn = self.players[0]
        self.phase = Turn.ROLLDICE
        self.turn_number = 0
        self.bank = {Resource.WHEAT: 20, Resource.ORE: 20, Resource.SHEEP: 20, Resource.BRICK: 20, Resource.WOOD: 20} #todo: custom bank. check these numbers
        self.building_costs = {Settlement.SETTLEMENT: {Resource.WHEAT: 1, Resource.SHEEP: 1, Resource.BRICK: 1, Resource.WOOD: 1},
                               Settlement.CITY: {Resource.ORE: 3, Resource.WHEAT: 2},
                               'road': {Resource.WOOD: 1, Resource.BRICK: 1}}

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

    def victory_points(self):
        #todo: longest road
        #todo: largest army
        #todo: dev cards
        victory_points = defaultdict(int)
        for vertex in self.graph.nodes:
            if vertex is not None and vertex.settlement is not None:
                victory_points[vertex.owner.name] += vertex.settlement.value
        return victory_points


#  **************** Placement methods ****************

    def can_place(self, player):
        if self.turn != player:
            return False, "It's not your turn!"
        if self.phase != Turn.BUILD:
            return False, "You're not in the build phase!"

        return True, ''

    def can_build(self, player, building):
        cost = self.building_costs[building]
        for resource, amount in cost.items():
            if player.resources[resource] < amount:
                return False, "Not enough resources"

        return True, ''

    def charge_building_costs(self, player, building):
        #TODO: BANK
        cost = self.building_costs[building]
        for resource, amount in cost.items():
            player.resources[resource] -= amount

    #TODO: TEST
    def place_road(self, v1, v2, player):
        success, error = self.can_place(player)
        if not success:
            return False, error

        success, error = self.can_build(player, 'road')
        if not success:
            return False, error

        if 'owner' in self.graph[v1][v2]:
            return False, "There's already a road there!"

        can_place = False

        #find adjacent settlement
        if v1.owner == player or v2.owner == player:
            can_place = True

        #find adjacent road
        if not can_place:
            for _, _, edge_data in self.graph.edges([v1, v2], data=True):
                if 'owner' in edge_data and edge_data['owner'] == player:
                    can_place = True
                    break

        if not can_place:
            return False, "You must have an adjacent settlement or road"

        #success
        self.graph[v1][v2]['owner'] = player
        self.graph[v1][v2]['type'] = 'road'
        self.charge_building_costs(player, 'road')

        return True, None

    def place_settlement(self, vertex, player, must_connect_to_road=True):
        #todo: actual game setup
        if self.turn_number < 2:
            must_connect_to_road = False

        success, error = self.can_place(player)
        if not success:
            return False, error

        success, error = self.can_build(player, Settlement.SETTLEMENT)
        if not success:
            return False, error

        if vertex.owner:
            return False, "There's already a settlement there!"

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
        self.charge_building_costs(player, Settlement.SETTLEMENT)

        return True, None

    def place_city(self, vertex, player):
        success, error = self.can_place(player)
        if not success:
            return False, error

        success, error = self.can_build(player, Settlement.CITY)
        if not success:
            return False, error

        if vertex.owner != player:
            return False, "You must own this settlement to upgrade it to a city"

        if vertex.settlement != Settlement.SETTLEMENT:
            return False, "You must build a settlement before you can build a city"

        #success
        vertex.settlement = Settlement.CITY
        self.charge_building_costs(player, Settlement.CITY)

        return True, None

#  **************** Turn methods ****************

    #TODO: test
    #todo: validate player is in roll phase
    #TODO: subtract from bank (and check if we have enough)
    def roll_dice(self):
        roll = random.randint(1, 6) + random.randint(1, 6)
        #todo: robber
        for row in self.tiles:
            for tile in row:
                #we shouldn't have numbers on our excepted_resources, but just in case...
                if tile is None or tile.resource_number != roll or tile.resource_type in Resource.excepted_resources():
                    continue
                for vertex in tile.vertices:
                    if vertex.owner:
                        amount = 1 if vertex.settlement == Settlement.SETTLEMENT else 2 if vertex.settlement == Settlement.CITY else 0
                        vertex.owner.resources[tile.resource_type] += amount

        #TODO: TRADING PHASE
        self.phase = Turn.BUILD
        return roll, ''


    def end_turn(self):
        if self.turn == self.players[-1]:
            self.turn_number += 1

        index = self.players.index(self.turn)
        index = (index + 1) % len(self.players)
        self.turn = self.players[index]
        self.phase = Turn.ROLLDICE

    def is_player_turn(self, player_name):
        player = self.player_with_name(player_name)
        return self.turn == player

#  **************** Serialization methods ****************

    def serialized_settlements(self):
        return [vertex.serialize() for vertex in self.graph.nodes if vertex is not None and vertex.settlement is not None]

    def serialized_roads(self):
        edges = []
        for (v1, v2, data) in self.graph.edges(data=True):
            if data:
                edge = {"v1": v1.location,
                        "v2": v2.location,
                        "owner": data["owner"].name,
                        "type": data["type"]}
                edges.append(edge)
        return edges
