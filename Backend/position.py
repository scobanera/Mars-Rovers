import json
from flask import jsonify

class Position:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def turnRight(self):
        newDirection = {'N':'E', 'E':'S', 'S':'W', 'W':'N'}
        self.direction = newDirection[self.direction]

    def turnLeft(self):
        newDirection = {'N':'W', 'W':'S', 'S':'E', 'E':'N'}
        self.direction = newDirection[self.direction]

    def nextX(self):
        next = {'N':self.x, 'S':self.x, 'E':self.x + 1, 'W':self.x - 1}
        return next[self.direction]

    def nextY(self):
        next = {'N':self.y + 1, 'S':self.y - 1, 'E':self.y, 'W':self.y}
        return next[self.direction]