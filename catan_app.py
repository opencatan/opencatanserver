from flask import Flask, jsonify, request
from enum import Enum
from graph import Vertex, Graph
import networkx as nx
from classes import Turn, Settlement, Resource
from tile import Tile, generate_board
import sys
from catan import Catan
from flask_cors import CORS

# tiles = [[Tile(Resource.WOOD, 3), Tile(Resource.ORE, 1),    Tile(Resource.WHEAT, 2)],
#          [None, Tile(Resource.WOOD, 3), Tile(Resource.BRICK, 4)],
#          [Tile(Resource.WOOD, 3), Tile(Resource.DESERT, 0), Tile(Resource.SHEEP, 4)]]

players = ['A', 'B']

def serialize_game(game):
    ret_dict = {}
    ret_dict['players'] = [player.serialize() for player in game.players]
    ret_dict['board'] = tiles_to_jsonifiable(game.tiles)
    ret_dict['robber'] = game.robber.serialize()
    ret_dict['turn'] = { 'player': game.turn.name,
                         'phase': game.phase.value}
    ret_dict['settlements'] = game.serialized_settlements()
    ret_dict['roads'] = game.serialized_roads()
    return ret_dict

def tiles_to_jsonifiable(tiles):
    json_tiles = []
    for row in tiles:
        json_row = []
        for _hex in row:
            if _hex is None:
                json_row.append(None)
                continue
            tile_dict = {'resource_type': _hex.resource_type.value,
            'resource_number': _hex.resource_number}
            json_row.append(tile_dict)
        json_tiles.append(json_row)
    return json_tiles

app = Flask(__name__)
CORS(app)

game = Catan(generate_board(3, 5), players)


@app.route("/")
def game_state():
   return jsonify(serialize_game(game))

@app.route("/generate/<top_width>/<middle_width>")
def generate(top_width, middle_width):
    global game
    game = Catan(generate_board(int(top_width), int(middle_width)), players)
    return jsonify(serialize_game(game))

#todo: error handling
@app.route("/place/<object>/<i>/<j>/<k>")
def place(object, i, j, k):
    player = request.args['player']
    i = int(i)
    j = int(j)
    k = int(k)
    player = game.player_with_name(player)
    if player is None:
        #todo handle error
        return "player is none"

    vertex = game.tiles[i][j].vertices[k]
    if vertex is None:
        #todo handle error
        return "vertex is none"

    if object == "settlement":
        #todo error handling
        success, error = game.place_settlement(vertex, player, must_connect_to_road=False)
    elif object == "city":
        success, error = game.place_city(vertex, player)
    elif object == "road":
        vertex2 = game.tiles[i][j].vertices[(k+1) % 6]
        success, error = game.place_road(vertex, vertex2, player)
    else:
        success, error = False, "No object specified"

    #todo: error handling lol
    return error if error is not None else ""

@app.route("/end_turn")
def end_turn():
    game.end_turn()
    return ""

@app.route("/roll_dice")
def roll_dice():
    roll, error = game.roll_dice()
    return str(roll)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
