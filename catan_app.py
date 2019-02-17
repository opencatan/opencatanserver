from flask import Flask, jsonify
from enum import Enum
from graph import Vertex, Graph
import networkx as nx
from classes import Turn, Settlement, Resource
from tile import Tile
from player import Player
import sys
from catan import Catan

tiles = [[Tile(Resource.ORE, 1),    Tile(Resource.WHEAT, 2)], 
         [Tile(Resource.WOOD, 3), Tile(Resource.BRICK, 4)]]

players = [Player('A'), Player('B')]

def serialize_game(game):
    ret_dict = {}
    ret_dict['players'] = [player.serialize() for player in game.players]
    ret_dict['board'] = tiles_to_jsonifiable(game.tiles)
    ret_dict['robber'] = game.robber.serialize()
    ret_dict['turn'] = { 'player': game.turn.name,
                         'phase': game.phase}
    return ret_dict

def tiles_to_jsonifiable(tiles):
    json_tiles = []
    for row in tiles:
        json_row = []
        for _hex in row:
            if _hex is None:
                json_row.append(None)
                continue
            resource_type = _hex.resource_type.value
            resource_number = _hex.resource_number
            json_row.append((resource_type, resource_number))
        json_tiles.append(json_row)
    return json_tiles

game = Catan(tiles, players)
# vertex_set = set([v for v in [tile.vertices for tile in [row for row in game.tiles]]])
vertex_set = set()
for row in game.tiles:
    for tile in row:
        if tile is None:
            continue
        for v in tile.vertices:
            vertex_set.add(v)

app = Flask(__name__)

@app.route("/")
def game_state():
    return jsonify(serialize_game(game))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)