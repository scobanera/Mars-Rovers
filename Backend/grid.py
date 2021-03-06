# -----------------------------------------------------------
# Plateau grid
#
# The plateau is organized using a grid that goes from (0, 0)
# to (max_x - 1, max_y - 1).
# -----------------------------------------------------------

from position import Position

class Grid:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

    def contains(self, position):
        return position.x >= 0 and position.x < self.max_x and position.y >= 0 and position.y < self.max_y