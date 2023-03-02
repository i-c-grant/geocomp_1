from .Geom import Geom
from .Shape import Shape
from .Point import Point


class Square(Shape):
    def __init__(self, blueprint: list):

        # Blueprint is two points corresponding to diagonal corners
        self.geomType = "Square"

        # Shape init will use Square's construct() function to set the
        # full description of the Square
        super().__init__(blueprint)

    def constructPoints(self, blueprint):
        """Takes a list of two Points representing diagonal corners of the
        square. Returns a list containing Points representing all four
        corners."""
        # Raise TypeError exception if blueprint is not a list or if it
        # contains objects other than points
        if type(blueprint) != list:
            raise TypeError
        else:
            for obj in blueprint:
                if type(obj) != Point:
                    raise TypeError

        # Raise ValueError exception if blueprint list has the wrong
        # number of elements or if it conatins two identical points
        if len(blueprint) != 2 or blueprint[0].isEquivalent(blueprint[1]):
            raise ValueError

        corners = [None] * 4

        # Assign points in blueprint to first and third places in the
        # list of corners. Since blueprint points are diagonal points,
        # this list order makes more sense
        corners[0] = blueprint[0]
        corners[2] = blueprint[1]

        center = Point(corners[0].midpoint(corners[2]))

        xdiff = center.x - corners[0].x
        ydiff = center.y - corners[0].y

        corners[1] = Point([center.x + ydiff, center.y - xdiff])
        corners[3] = Point([center.x - ydiff, center.y + xdiff])

        del center  # delete temporary center Point

        return corners

    def constructProperties(self, blueprint: list, points: list):
        props : dict = {}
        props["side"] = points[0].distance(points[1])
        props["area"] = props["side"] ** 2
        center = Point(self.points[0].midpoint(self.points[1]))
        props["center"] = center
        return props

        
        
        
