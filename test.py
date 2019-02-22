import sys
# import matplotlib.pyplot as plt
import networkx as nx
from enum import Enum
from graph import Vertex, Graph
from classes import Turn, Settlement, Resource
from catan import Catan
from tile import Tile
from player import Player

a = Tile('A',1)
b = Tile('B',1)
c = Tile('C',1)
d = Tile('D',1)
e = Tile('E',1)
f = Tile('F',1)
tiles = [[a,b],[c,d],[e,f]]

# nx.draw(catan.graph)
# plt.show()

def test_place_settlement_and_city(): #todo: make more "unitable" instead of a mega-test
    catan = Catan(tiles, ["ben", "bops"])

    #special placements (beginning of game)
    success, error = catan.place_settlement(c.vertices[0], catan.players[0], must_connect_to_road=False)
    assert(success)
    success, error = catan.place_settlement(c.vertices[2], catan.players[1], must_connect_to_road=False)
    assert(success)

    #test adjacency
    success, error = catan.place_settlement(c.vertices[3], catan.players[0], must_connect_to_road=False)
    assert(not success)
    #test adjacency
    success, error = catan.place_settlement(c.vertices[3], catan.players[1], must_connect_to_road=False)
    assert(not success)

    #build roads for ben
    catan.place_road(c.vertices[0], c.vertices[5], catan.players[0])
    catan.place_road(c.vertices[4], c.vertices[5], catan.players[0])

    #test road adjacency
    success, error = catan.place_settlement(c.vertices[4], catan.players[1])
    assert(not success)
    #test road adjacency
    success, error = catan.place_settlement(c.vertices[4], catan.players[0])
    assert(success)

    success, error = catan.place_city(c.vertices[4], catan.players[1])
    assert(not success)
    success, error = catan.place_city(c.vertices[3], catan.players[1])
    assert(not success)
    success, error = catan.place_city(c.vertices[4], catan.players[0])
    assert(success)

    # print(catan.serialized_settlements())
    # print(catan.serialized_roads())
    # print(catan.player_with_name('ben'))




if __name__ == "__main__":
    test_place_settlement_and_city()


# print (c.vertices)
# print (catan.graph.nodes[6])
# catan.place_city(6, 'nick')
# catan.place_settlement(6, 'nick')
# print (catan.graph.nodes[6])
# catan.place_city(6, 'nick')
# print (catan.graph.nodes[6])
#
# attrs = {0: {'attr1': 20, 'attr2': 'nothing'}, 1: {'attr2': 3}}
#nx.set_node_attributes(catan.graph, {6: {'has' : ['settlement', 'nick']}})
#print (catan.graph[6]['has'])


#catan.graph = nx.path_graph(3)
#attrs = {0: {'attr1': ['hi'], 'attr2': 'nothing'}, 1: {'attr2': 3}}
#attrs = {6: {'has': ['settlement', 'nick']}}
#nx.set_node_attributes(catan.graph, attrs)
#print (catan.graph.nodes[6])
