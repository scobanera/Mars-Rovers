from position import Position
from grid import Grid


class Rover:
    def __init__(self, position, grid):
        self.grid = grid
        self.position = position

    def move(self):
        nextPos = Position(self.position.nextX(), self.position.nextY(), self.position.direction)
        if(self.grid.contains(nextPos)):
            self.position = nextPos
            return True

        return False

    def rotate(self, turn):
        if (turn == 'L'):
            self.position.turnLeft()
        if (turn == 'R'):
            self.position.turnRight()

    def execute(self, commands):
        for command in commands:
            if (command in ['L', 'R']):
                self.rotate(command)
            if (command == 'M'):
                if self.move() is False: return