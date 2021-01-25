import os
import pymysql
import logging
from flask import jsonify
from grid import Grid
from rover import Rover
from position import Position

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    conn = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)

    return conn

def get_grid():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT max_x, max_y FROM plateau WHERE plateau_id = 1;')
        plateau = cursor.fetchone()
    conn.close()
    return Grid(plateau["max_x"], plateau["max_y"])


def update_grid(grid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE plateau SET max_x=%s, max_y=%s WHERE plateau_id = 1;', (grid.max_x, grid.max_y))
    conn.commit()
    conn.close()


def get_rovers():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM rovers;')
        rovers = cursor.fetchall()
        if result > 0:
            got_rovers = jsonify(rovers)
        else:
            got_rovers = 'No Rovers in DB'
    conn.close()
    return got_rovers


def get_rover(id):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT pos_x, pos_y, direction FROM rovers WHERE rover_id = %s;', (id))
        result_value = cursor.fetchone()
        if result > 0:
            pos = Position(result_value["pos_x"], result_value["pos_y"], result_value["direction"])
            got_rover = Rover(pos, None)
        else:
            got_rovers = None
    conn.close()
    return got_rover


def add_rover(rover):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO rovers (pos_x, pos_y, direction) VALUES(%s, %s, %s);', (rover.position.x, rover.position.y, rover.position.direction))
    conn.commit()
    id = cursor.lastrowid
    conn.close()
    return id


def update_rover(id, rover):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE rovers SET pos_x=%s, pos_y=%s, direction=%s WHERE rover_id=%s;', (rover.position.x, rover.position.y, rover.position.direction, id))
    conn.commit()
    conn.close()
    return "Rover successfully updated."


def delete_rovers():
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM rovers;')
    conn.commit()
    conn.close()
    return "Rover successfully deleted."