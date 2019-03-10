from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from enum import Enum
from graph import Vertex, Graph
import networkx as nx
from classes import Turn, Settlement, Resource
from tile import Tile, generate_board
import sys
from catan import Catan
from flask_cors import CORS
from functools import wraps
import os
import pickle
from bson.binary import Binary

players = ['A', 'B']
app = Flask(__name__)
CORS(app)

try:
    app.config["MONGO_URI"] = os.environ["MONGODB_URI"]
except KeyError:
    app.config["MONGO_URI"] = "mongodb://localhost:27017/catan"
mongo = PyMongo(app)

game_id = 1

### client <-> server serialization ###

def serialize_game(game):
    ret_dict = {}
    ret_dict['players'] = [player.serialize() for player in game.players]
    ret_dict['board'] = tiles_to_jsonifiable(game.tiles)
    ret_dict['robber'] = game.robber.serialize()
    ret_dict['turn'] = { 'player': game.turn.name,
                         'phase': game.phase.value}
    ret_dict['settlements'] = game.serialized_settlements()
    ret_dict['roads'] = game.serialized_roads()
    ret_dict['victory_points'] = game.victory_points()
    ret_dict['offers'] = game.serialize_offers()
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

### server <-> database access

def find_game(id):
    try:
        game_data = mongo.db.games.find_one({"id": id})['data']
        game = pickle.loads(game_data)
        return game
    except:
        return None

def store_game(id, game):
    #todo: don't use pickle
    game_data = Binary(pickle.dumps(game))
    d = {"id": id,
         "data": game_data}
    mongo.db.games.replace_one({"id": id}, d, upsert=True)

### view decorators ###

def read_game(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        game = find_game(game_id)
        kwargs['game'] = game
        return f(*args, **kwargs)
    return wrap

def read_write_game(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        game = find_game(game_id)
        kwargs['game'] = game
        ret_val = f(*args, **kwargs)
        store_game(game_id, game)
        return ret_val
    return wrap

def validate_player(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        player = None
        print(kwargs['game'])
        print(request.args['player'])
        if 'player' in request.args and kwargs['game'].is_player_turn(request.args['player']):
            return f(*args, **kwargs)
        else:
            return "It's not your turn!"
    return wrap

### views ###

@app.route("/")
@read_game
def game_state(game=None):
    if game is not None:
       return jsonify(serialize_game(game))
    else:
       return "no game"

@app.route("/generate/<top_width>/<middle_width>")
def generate(top_width, middle_width):
    game = Catan(generate_board(int(top_width), int(middle_width)), players)
    store_game(game_id, game)
    return jsonify(serialize_game(game))

#todo: error handling
@app.route("/place/<object>/<i>/<j>/<k>")
@read_write_game
@validate_player
def place(object, i, j, k, game=None):
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
        success, error = game.place_settlement(vertex, player)
    elif object == "city":
        success, error = game.place_city(vertex, player)
    elif object == "road":
        vertex2 = game.tiles[i][j].vertices[(k+1) % 6]
        success, error = game.place_road(vertex, vertex2, player)
    else:
        success, error = False, "No object specified"

    #todo: error handling lol
    return error if error is not None else ""


#todo: error handling
@app.route("/offer/make")
@read_write_game
@validate_player
def make_offer(game=None):
    player_maker = game.player_with_name(request.args['player_maker'])
    resources_from = request.args['resources_from']
    resources_to = request.args['resources_to']
    success, error = game.create_offer(player_maker, resources_from, resources_to)
    #todo: error handling lol
    return error if error is not None else ""


#todo: error handling
@app.route("/offer/take")
@read_write_game
@validate_player
def take_offer(game=None):
    player_taker = game.player_with_name(request.args['player_taker'])
    offer_id = request.args['offer_id']
    success, error = game.take_offer(player_taker, offer_id)
    #todo: error handling lol
    return error if error is not None else ""


@app.route("/end_turn")
@read_write_game
@validate_player
def end_turn(game=None):
    game.end_turn()
    return ""

@app.route("/roll_dice")
@read_write_game
@validate_player
def roll_dice(game=None):
    roll, error = game.roll_dice()
    return str(roll)

@app.route("/test")
def test():
    games = mongo.db.games
    data = {"foo": "bar"}
    id = games.insert_one(data).inserted_id
    print("id", id)
    return "hi"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
