# -----------------------------------------------------------
# Flask server for the Mars Rover API
#
# (C) 2020 Santiago Cobanera, Buenos Aires, Argentina.
# Released under GNU Public License (GPL)
# -----------------------------------------------------------

import flask
import logging

from flask import request, jsonify, make_response
from database import *
from position import Position
from grid import Grid
from rover import Rover

app = flask.Flask(__name__)

@app.after_request
def apply_caching(response):
    """ Attach Access Control headers to the response after the same has been created. """
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    return response


@app.route('/', methods=['GET'])
def home():
    """ Home path to test the API is alive and clients were able to connect successfully. """
    return "Mars API is running :)"


@app.route('/rovers/list', methods=['GET'])
def rovers_list():
    """ List all the rovers that are currently stored in the database. """
    return make_response(get_rovers())


@app.route('/rovers/create', methods=['POST'])
def rovers_create():
    """ Create and store a rover at the given position and direction. """
    params = request.json
    if all(key in params for key in ("pos_x", "pos_y", "direction")):
        pos = Position(params["pos_x"], params["pos_y"], params["direction"])
        rover_id = add_rover(Rover(pos, None))
        response = make_response(jsonify({"id":rover_id}), 200)
    else:
        response = make_response('Cannot create rover - Missing information', 400)

    return response


@app.route('/rovers/<id>/move', methods=['POST'])
def rovers_move(id):
    """ Move the rover according to the provided set of commands. """
    rover = get_rover(id)
    if (rover is None):
        return make_response('Rover not found', 400)

    params = request.json
    if ("commands" not in params):
        return make_response('Missing commands', 400)

    rover.grid = get_grid()
    rover.execute(params["commands"])
    update_rover(id, rover)
    return make_response(jsonify(rover.position.__dict__))


@app.route('/rovers/delete', methods=['POST'])
def rovers_delete():
    """ Delete all rovers in the database. """
    return delete_rovers()


@app.route('/grid/size', methods=['GET'])
def grid_size():
    """ Returns the size of the grid as a pair of x and y. """
    grid = get_grid()
    return make_response(jsonify(grid.__dict__))


@app.route('/grid/resize', methods=['POST'])
def grid_resize():
    """ Resizes the grid to the specified new size. """
    params = request.json
    if all(key in params for key in ("max_x", "max_y")):
        grid = Grid(params["max_x"], params["max_y"])
        update_grid(grid)

        return make_response('Grid succesfully updated')
    else:
        return make_response('Grid not updated - Missing parameters', 400)

if __name__ == '__main__':
    app.run()