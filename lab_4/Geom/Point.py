from .Geom import Geom
import math

class Point(Geom):
    def __init__(self, coords: list):
        """Creates a point from a list in format [x, y]."""
        self.geomType = "Point"
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.coords = [self.x, self.y]

        super().__init__()

    def isEquivalent(self, other):  # other is another point
        return self.x == other.x and self.y == other.y

    def midpoint(self, other):
        """Returns list with the coordinates of the line segment formed by
        self and other (another point)

        """
        if type(self) != Point or type(other) != Point:
            raise TypeError
        
        midx = (self.x + other.x) / 2
        midy = (self.y + other.y) / 2
        return [midx, midy]
    

    def distance(self, other):
        """Returns distance between self and another point."""
        if type(self) != Point or type(other) != Point:
            raise TypeError

        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
