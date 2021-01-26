# -----------------------------------------------------------
# Rover current position.
#
# The rover current position is composed by the (x, y) coordinates
# on the grid, as well as a direction.
# -----------------------------------------------------------

class Position:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def turnRight(self):
        # Mapping direction after rotating 90 degrees right for each possible cardinal direction.
        newDirection = {'N':'E', 'E':'S', 'S':'W', 'W':'N'}
        self.direction = newDirection[self.direction]

    def turnLeft(self):
        # Mapping direction after rotating 90 degrees left for each possible cardinal direction.
        newDirection = {'N':'W', 'W':'S', 'S':'E', 'E':'N'}
        self.direction = newDirection[self.direction]

    def nextX(self):
        # If direction is North our South, x coordinate remains unchanged.
        # If it's East or West, it will increase or decrease respectively.
        next = {'N':self.x, 'S':self.x, 'E':self.x + 1, 'W':self.x - 1}
        return next[self.direction]

    def nextY(self):
        # If direction is East our West, y coordinate remains unchanged.
        # If it's North or South, it will increase or decrease respectively.
        next = {'N':self.y + 1, 'S':self.y - 1, 'E':self.y, 'W':self.y}
        return next[self.direction]