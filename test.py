import sys
import matplotlib.pyplot as plt
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

catan = Catan(tiles, ["name1", "name2"])
print (catan.graph.nodes)
print (catan.graph.edges)
nx.draw(catan.graph)
plt.show()

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
